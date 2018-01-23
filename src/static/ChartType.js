Chart.defaults.symmetricErrorLine = Chart.defaults.line;

var custom = Chart.controllers.line.extend({
    draw: function(ease) {
        Chart.controllers.line.prototype.draw.call(this, ease);
        var meta = this.getMeta();
        for (m in meta.data) {
            var pt0 = meta.data[m];
	    var point = pt0._view
	    var chart = this.chart;
	    var height = chart.chartArea.bottom - chart.chartArea.top;
	    var ctx = this.chart.chart.ctx;
	    var datasets = chart.config.data.datasets[pt0._datasetIndex];
	    var error = datasets.error;
            var values = datasets.data;
	    var p = height / pt0._yScale.max;
            var width = pt0._yScale.maxWidth / 4;
            var true_error = p * error[pt0._index];
            var smallest = point.y + true_error;
            if (this.chart.config.options.scales.yAxes[0].ticks.beginAtZero) {
                if (smallest >= chart.chartArea.bottom) {
                    smallest = chart.chartArea.bottom;
                }
            }
            var color = datasets.errorColor;
            ctx.beginPath();
            ctx.strokeStyle = color;
            ctx.moveTo(point.x, point.y);
            ctx.lineTo(point.x, smallest);
            ctx.lineTo(point.x, point.y - true_error);
            ctx.moveTo(point.x, point.y - true_error);
            ctx.lineTo(point.x - width, point.y - true_error);
            ctx.lineTo(point.x + width, point.y - true_error);
            ctx.moveTo(point.x, smallest);
            ctx.lineTo(point.x - width, smallest);
            ctx.lineTo(point.x + width, smallest);
            ctx.stroke();
        }
    }
});

Chart.controllers.symmetricErrorLine = custom;
Chart.defaults.symmetricErrorBar = Chart.defaults.bar;

var custom2 = Chart.controllers.bar.extend({
    draw: function(ease) {
        Chart.controllers.bar.prototype.draw.call(this, ease);
        var meta = this.getMeta();
        for (m in meta.data) {
            var pt0 = meta.data[m];
            var point = pt0._view
            var chart = this.chart;
            var height = chart.chartArea.bottom - chart.chartArea.top;
            var ctx = this.chart.chart.ctx;
            var datasets = chart.config.data.datasets[pt0._datasetIndex];
            var error = datasets.error;
            var values = datasets.data;
            var p = height / pt0._yScale.max;
            var width = point.width / 4;
            var true_error = p * error[pt0._index];
            var smallest = point.y + true_error;
            if (this.chart.config.options.scales.yAxes[0].ticks.beginAtZero) {
                if (smallest >= chart.chartArea.bottom) {
                    smallest = chart.chartArea.bottom;
                }
            }
            var color = datasets.errorColor;
            ctx.beginPath();
            ctx.strokeStyle = color;
            ctx.moveTo(point.x, point.y);
            ctx.lineTo(point.x, smallest);
            ctx.lineTo(point.x, point.y - true_error);
            ctx.moveTo(point.x, point.y - true_error);
            ctx.lineTo(point.x - width, point.y - true_error);
            ctx.lineTo(point.x + width, point.y - true_error);
            ctx.moveTo(point.x, smallest);
            ctx.lineTo(point.x - width, smallest);
            ctx.lineTo(point.x + width, smallest);
            ctx.stroke();
        }
    }
});

Chart.controllers.symmetricErrorBar = custom2;
