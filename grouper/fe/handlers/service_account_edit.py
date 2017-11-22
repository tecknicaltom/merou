from grouper.fe.forms import ServiceAccountEditForm
from grouper.fe.util import GrouperHandler
from grouper.models.group import Group
from grouper.models.service_account import ServiceAccount
from grouper.service_account import can_manage_service_account, edit_service_account


class ServiceAccountEdit(GrouperHandler):
    def get(self, group_id=None, name=None, account_id=None, accountname=None):
        group = Group.get(self.session, group_id, name)
        if not group:
            return self.notfound()
        service_account = ServiceAccount.get(self.session, account_id, accountname)
        if not service_account:
            return self.notfound()

        if not can_manage_service_account(self.session, service_account, self.current_user):
            return self.forbidden()

        form = ServiceAccountEditForm(obj=service_account)

        self.render(
            "service-account-edit.html", service_account=service_account, group=group, form=form,
        )

    def post(self, group_id=None, name=None, account_id=None, accountname=None):
        group = Group.get(self.session, group_id, name)
        if not group:
            return self.notfound()
        service_account = ServiceAccount.get(self.session, account_id, accountname)
        if not service_account:
            return self.notfound()

        if not can_manage_service_account(self.session, service_account, self.current_user):
            return self.forbidden()

        form = ServiceAccountEditForm(self.request.arguments, obj=service_account)
        if not form.validate():
            return self.render(
                "service-account-edit.html", service_account=service_account, group=group,
                form=form, alerts=self.get_form_alerts(form.errors)
            )

        edit_service_account(self.session, self.current_user, service_account,
                             form.data["description"], form.data["machine_set"])

        return self.redirect("/groups/{}/service/{}".format(
            group.name, service_account.user.username))
