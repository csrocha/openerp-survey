// static/src/js/online.js
openerp.zondaggio = function(instance) {

    instance.zondaggio = {};

    var module = instance.zondaggio;

    openerp_zondaggio_models(instance,module);    // import models.js
    openerp_zondaggio_widgets(instance,module);    // import screens.js

    instance.web.client_actions.add('questionnaire.ui', 'instance.zondaggio.questionnaire_ui');
};

/*
on_change_select_one = function(widget) {
    if (widget.type=='radio') {
        var widget_parent = $(_.str.sprintf("input[type='hidden'][class='%s']", widget.name))[0];
        widget_parent.value = widget.alt;
    }
};
*/

// vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
