var widgets = require('@jupyter-widgets/base');
var _ = require('lodash');

// When serialiazing the entire widget state for embedding, only values that
// differ from the defaults will be specified.
var RawCanvasModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
        _model_name : 'RawCanvasModel',
        _view_name : 'RawCanvasView',
        _model_module : 'fastcanvas',
        _view_module : 'fastcanvas',
        _model_module_version : '0.1.0',
        _view_module_version : '0.1.0',
        value : null
    })
});

// Custom View. Renders the widget model.
var RawCanvasView = widgets.DOMWidgetView.extend({
    render: function() {
        this.canvas = document.createElement('canvas');
        this.el.append(this.canvas);
        this.data_changed();
        this.model.on('change:data', this.data_changed, this);
    },

    data_changed: function() {
        var val = this.model.get('data')
        if (val !== null && val.shape.length && val.shape[0] > 0)
        {
            if (this.canvas.width != val.shape[1])
            {
                this.canvas.width = val.shape[1];
                this.canvas.height = val.shape[0];
            }
            var imd = new ImageData(new Uint8ClampedArray(val.buffer.buffer), val.shape[1]);
            var ctx = this.canvas.getContext("2d");
            ctx.putImageData(imd, 0, 0);
        }
    }
});

module.exports = {
    RawCanvasModel: RawCanvasModel,
    RawCanvasView: RawCanvasView
};
