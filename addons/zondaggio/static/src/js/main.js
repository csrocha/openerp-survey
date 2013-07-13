// static/src/js/online.js
openerp.zondaggio = function(instance) {

    instance.zondaggio = {};

    var module = instance.zondaggio;

    openerp_zondaggio_models(instance,module);    // import models.js
    openerp_zondaggio_widgets(instance,module);    // import screens.js

    instance.web.client_actions.add('questionnaire.ui', 'instance.zondaggio.questionnaire_ui');
};

// vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
