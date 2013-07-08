// static/src/js/first_module.js
openerp.zondaggio = function (instance) {
    console.log("Module loaded");
    instance.web.client_actions.add('online.action', 'instance.zondaggio.action');
    instance.zondaggio.action = instance.web.Widget.extend({
	template: 'zondaggio.action'
    });
};
