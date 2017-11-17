from .models import TrafficDivider, Experiment
from django.shortcuts import get_object_or_404

def ab_init(self):
    # If in Generic Views
    if self:
        # get_or_create return tuple, so we need only first element
        divider = TrafficDivider.objects.get_or_create(page_title=self.page_name)[0]
        experiment = Experiment.objects.get_or_create(page_title=self.page_name, divider=divider)[0]

        if experiment.is_active:
            # set sessions names using page_name variable
            session_name = 'session_' + self.page_name
            get_session_name = self.request.session.get(session_name)

            # if user already saw this in default version
            if get_session_name == True:
                pass
            # if user already saw page in alternative version
            elif get_session_name == False:
                # set alternative template file
                self.template_name = self.alternative_template_name
            # if calc_page not exist in session, set user to one of them
            if get_session_name == None:
                if divider.divider == True:
                    self.request.session[session_name] = False
                    # add to alternative entered +1
                    experiment.alternative_entered += 1
                    # toggle divider
                    divider.divider = False

                    # saving
                    experiment.save()
                    divider.save()
                    # set alternative template file
                    self.template_name = self.alternative_template_name
                else:
                    self.request.session[session_name] = True
                    # just add to entered +1 and save
                    divider.divider = True
                    # add to entered variable 1
                    experiment.entered += 1
                    # save
                    experiment.save()
                    divider.save()

def method_ab_init(request, template_name, alternative_template_name, page_name):
    # get_or_create return tuple, so we need only first element
    divider = TrafficDivider.objects.get_or_create(page_title=page_name)[0]
    experiment = Experiment.objects.get_or_create(page_title=page_name, divider=divider)[0]

    if experiment.is_active:
        # set sessions names using page_name variable
        session_name = 'session_' + page_name
        get_session_name = request.session.get(session_name)


        # if user already saw this in default version
        if get_session_name == True:
            pass
        # if user already saw page in alternative version
        elif get_session_name == False:
            # set alternative template file
            template_name = alternative_template_name
        # if calc_page not exist in session, set user to one of them
        if get_session_name == None:
            if divider.divider == True:
                request.session[session_name] = False
                # add to alternative entered +1
                experiment.alternative_entered += 1
                # toggle divider
                divider.divider = False
                # set alternative template file
                template_name = alternative_template_name
            else:
                request.session[session_name] = True
                # just add to entered +1 and save
                divider.divider = True
                # add to entered variable 1
                experiment.entered += 1

            # save
            experiment.save()
            divider.save()
    return template_name

def success_goal(self=None):
    # If in Generic Views
    if self:
        # get_or_create return tuple, so we need only first element
        divider = TrafficDivider.objects.get_or_create(page_title=self.page_name)[0]
        experiment = Experiment.objects.get_or_create(page_title=self.page_name, divider=divider)[0]

        if experiment.is_active:
            goal_session_name = 'session_success_' + self.page_name
            # A/B testing
            get_goal_session_name = self.request.session.get(goal_session_name)
            # if user not already saw this
            if get_goal_session_name == None:
                # if divider equal True, means user can add to success variable only in first version
                if divider.divider == True:
                    experiment.success += 1
                    # need to set something to know in the future - this user already push this button
                    self.request.session[goal_session_name] = True
                else:
                    experiment.alternative_success += 1
                    # need to set something to know in the future - this user already push this button
                    self.request.session[goal_session_name] = True

                experiment.save()

def method_success_goal(request, page_name):
    divider = TrafficDivider.objects.get_or_create(page_title=page_name)[0]
    experiment = Experiment.objects.get_or_create(page_title=page_name, divider=divider)[0]

    if experiment.is_active:
        goal_session_name = 'session_success_' + page_name
        # A/B testing
        get_goal_session_name = request.session.get(goal_session_name)
        # if user not already saw this
        if get_goal_session_name == None:
            # if divider equal True, means user can add to success variable only in first version
            if divider.divider == True:
                experiment.success += 1
                # need to set something to know in the future - this user already push this button
                request.session[goal_session_name] = True
            else:
                experiment.alternative_success += 1
                # need to set something to know in the future - this user already push this button
                request.session[goal_session_name] = True

            experiment.save()
