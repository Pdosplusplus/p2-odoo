openerp.agili = function (instance, local) {
    
    var QWeb = openerp.web.qweb;
    var _t = instance.web._t;
    var self = this;

    instance.web.ListView.include({
        
        render_buttons: function () {
            var self = this;
            var add_button = false;
            if (!this.$buttons) { // Ensures that this is only done once
                add_button = true;
            }
            this._super.apply(this, arguments); // Sets this.$buttons
            if (add_button) {
                this.$buttons.find('.agili_btn_print_report').click(this.proxy('do_the_job'));
                console.log("Surrender");
            }
        },

        do_the_job: function () {
            
            var self = this;
     
            var model = new instance.web.Model("agili.project");

            model.call("print_report", {context: new instance.web.CompoundContext()}).then(function (result) {
                //self.$el.append("<div>Hello " + result["hello"] + "</div>");
                // will show "Hello world" to the user
                self.do_action(result);
            });
        }

    });

};