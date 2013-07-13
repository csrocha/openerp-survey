// static/src/js/widgets.js
function openerp_zondaggio_widgets(instance, module){
    var QWeb = instance.web.qweb,
	_t = instance.web._t;

    module.questionnaire_ui = instance.web.Widget.extend({
        template: 'StyledView',
        init:function(parent,options){
                this._super(parent);
                options = options || { context: {} };
                this.session.questionnaire_context = options.context;
                this.questionnaire = new module.Questionnaire(this.session);
                this.questionnaire_widget = this;
            },
        start:function() {
            var self=this;
            return self.questionnaire.ready.done(function(){
                self.renderElement();
            });
        },
        get_name:function() {
            if (this.questionnaire.get('survey') == null) {
                return 'No defined'
            } else {
                return this.questionnaire.get('survey').name;
            }
        },
        get_description:function() {
            if (this.questionnaire.get('survey') == null) {
                return 'No defined'
            } else {
                return this.questionnaire.get('survey').description;
            }
        },
        get_nodes:function() {
            if (this.questionnaire.get('nodes') == null) {
                return []
            } else {
                return this.questionnaire.get('nodes');
            }
        },
        get_pages:function() {
            if (this.questionnaire.get('pages') == null) {
                return []
            } else {
                return this.questionnaire.get('pages');
            }
        }
    })

};

// vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
