from iati.models import Activity
from traceability.models import Chain, ChainLink, ChainError
from django.core.exceptions import ObjectDoesNotExist


def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False


class ChainRetriever():
    """
    Wrapper class for all chain building functionality

    """
    def __init__(self):
        self.links = []
        self.errors = []
        self.chain = None

    def retrieve_chains_by_publisher(self, publisher_iati_id):
        for activity in Activity.objects.filter(publisher__publisher_iati_id=publisher_iati_id):
            print activity
            self.retrieve_chain(activity)

    def retrieve_chain_by_activity_id(self, activity_id):
        activity = Activity.objects.get(iati_identifier=activity_id)
        self.retrieve_chain(activity)

    def retrieve_chain(self, root_activity):

        # delete old chain
        if Chain.objects.filter(root_activity=root_activity).count() > 0:
            Chain.objects.filter(root_activity=root_activity).delete()

        # create, is saved as self.chain
        self.create_chain(root_activity)
        
        # add root activity to the links
        self.add_link(root_activity, None, 'up', False)

        # walk the tree
        self.walk_the_tree(0)

        # save links
        for link in self.links:
            link.pop('iati_identifier', None)
            link.pop('checked', None)

        ChainLink.objects.bulk_create([ChainLink(**link) for link in self.links])

        # save errors
        ChainError.objects.bulk_create([ChainError(**error) for error in self.errors])

        # reinit
        self.links = []
        self.errors = []
        self.chain = None



    def walk_the_tree(self, loops):

        for link in self.links:
            if not link['checked']:
                link['checked'] = True
                self.get_activity_links(link['activity'])

        if contains(self.links, lambda x: x['checked'] == False):
            loops += 1
            self.walk_the_tree(loops) 


    def add_link(self, activity, parent, direction, checked):
        
        if not contains(self.links, lambda x: x['iati_identifier'] == activity.iati_identifier):

            self.links.append({
                'chain': self.chain,
                'activity': activity,
                'iati_identifier': activity.iati_identifier,
                'parent_activity': parent,
                'direction' : direction,
                'checked': checked
            })

    def add_error(self, iati_identifier_or_link_id, iati_element, message, level):

        self.errors.append({
            'chain': self.chain,
            'error_location': iati_identifier_or_link_id,
            'iati_element': iati_element,
            # 'iati_element_id': ,
            'message': message,
            'level': level
        })

    def create_chain(self, root_activity):
        # create chain
        chain = Chain(name=root_activity.title.narratives.all()[0].content, root_activity=root_activity)
        chain.save()
        self.chain = chain

    def get_activity_links(self, activity):
        """
        Apply rules defined in the technical design.

        Rule 1.
        If it has Incoming fund with provider-activity-id  
        Then add link to reference upstream activity
        Else if they have no correct provider-activity-id set, create a broken link warning/error
        

        Rule 2.
        If it has disbursements with receiver-activity-id
        Then add link that references downstream activity
        Else if they have no correct receiver-activity-id set, create a broken link warning/error


        Rule 3.   
        If it has children as related-activity
        Then add link that references downstream activity


        Rule 4.   
        If it has parents as related-activity
        Then add link that references upstream activity


        Rule 5.   
        If it has participating-orgs not mentioned in rule 1 and 2 
        Then, depending upon role, add as possibly missing upstream or downstream links
        Upstream on role is funder and org is not the reporter of his activity. Downstream on other roles?


        Rule 6.
        If it is mentioned as provider-activity-id in incoming funds of activities
        Then add link that reference as downstream activity (direction is upwards)


        Rule 7.
        If it is mentioned as receiver-activity-id in disbursements of activities
        Then add link that reference as upstream activity (direction is downwards)


        Rule 8. = rule 1 else
        If it has provider-orgs with incorrect/missing provider-activity-id.
        Then add as broken link


        Rule 9. = rule 2 else
        If it has receiver-orgs with incorrect/missing receiver-activity-id.
        Then add as broken link

        """

        # init 
        provider_org_refs = []
        receiver_org_refs = []

        # 1.
        for t in activity.transaction_set.filter(transaction_type='1'):
            try:
                provider_org = t.provider_organisation
                provider_org_refs.append(provider_org.ref)
            except ObjectDoesNotExist:
                self.add_error(activity.iati_identifier, 'transaction/provider-org', 'provider-org not set on incoming funds', 'error')
                continue

            if not provider_org.provider_activity_ref or provider_org.provider_activity_ref == '':
                self.add_error(activity.iati_identifier, 'transaction/provider-org/provider-activity-id', 'no provider activity given on incoming fund', 'error')
            elif not provider_org.provider_activity:
                self.add_error(activity.iati_identifier, 'transaction/provider-org', 'given provider activity does not exist on incoming fund', 'error')
            else:
                self.add_link(t.activity, provider_org.provider_activity, 'up', False)

        # 2.
        for t in activity.transaction_set.filter(transaction_type='3'):
            try:
                receiver_org = t.receiver_organisation
                receiver_org_refs.append(receiver_org.ref)
            except ObjectDoesNotExist:
                self.add_error(activity.iati_identifier, 'transaction/receiver-org', 'receiver-org not set on disbursement', 'error')
                continue
            if not receiver_org.receiver_activity_ref or receiver_org.receiver_activity_ref == '':
                self.add_error(activity.iati_identifier, 'transaction/receiver-org/receiver-activity-id', 'no receiver activity given on disbursement', 'error')
            elif not receiver_org.receiver_activity:
                self.add_error(activity.iati_identifier, 'transaction/receiver-org', 'receiver activity of disbursement wih identifier "{}" does not exist'.format(receiver_org.receiver_activity_ref), 'warning')
            else:
                self.add_link(t.activity, receiver_org.receiver_activity, 'up', False)


        # 3 and 4.
        for ra in activity.relatedactivity_set.all():

            # parent
            if ra.type.code == '1':
                if not ra.ref_activity:
                    self.add_error(activity.iati_identifier, 'related-activity/ref', 'given parent related activity {} does not exist'.format(ra.ref), 'error')
                else:
                    self.add_link(activity, ra.ref_activity, 'up', False)
            # child
            elif ra.type.code == '2':
                if not ra.ref_activity:
                    self.add_error(activity.iati_identifier, 'related-activity/ref', 'given child related activity {} does not exist'.format(ra.ref), 'error')
                else:
                    self.add_link(ra.ref_activity, activity, 'down', False)

        # 4.
        # DONE IN #3.



        # cache for #5
        for t in activity.transaction_set.filter(transaction_type='4'):
            try:
                receiver_org = t.receiver_organisation
                receiver_org_refs.append(receiver_org.ref)
            except ObjectDoesNotExist:
                continue

        # 5.
        for ra in activity.participating_organisations.all():
            # for role funding, check if in incoming funds
            if ra.role.code == '1' and not ra.ref in provider_org_refs:
                self.add_error(activity.iati_identifier, 'participating-org', '{} is given as funder but there are no incoming funds from this organisation ref'.format(ra.ref), 'warning')

            # for role implementing, check if in disbursements or expenditures
            elif ra.role.code == '4' and not ra.ref in receiver_org_refs:
                self.add_error(activity.iati_identifier, 'participating-org', '{} is given as implementer but there are no disbursements nor expenditures from this organisation ref'.format(ra.ref), 'warning')


        # 6. 
        for a in Activity.objects.filter(transaction__transaction_type="1", transaction__provider_organisation__provider_activity_ref=activity.iati_identifier).distinct():
            self.add_link(a, activity, 'up', False)

        # 7.
        for a in Activity.objects.filter(transaction__transaction_type="3", transaction__receiver_organisation__receiver_activity_ref=activity.iati_identifier).distinct():
            self.add_link(a, activity, 'down', False)

        # 8.
        # DONE IN #1

        # 9.
        # DONE IN #2






