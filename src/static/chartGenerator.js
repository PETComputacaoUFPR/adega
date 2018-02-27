var colors = {
    red: {
        border: 'rgba(158, 22, 22, 1)',
        fill: 'rgba(252, 22, 22, 1)'
    },
    blue: {
        border: 'rgba(31, 110, 239, 1)',
        fill: 'rgba(151, 187, 205, 1)'
    },
    green: {
        border: 'rgba(28, 188, 47, 1)',
        fill: 'rgba(28, 188, 47, 0.2)'
    },
    purple: {
        border: 'rgba(112, 4, 244, 1)',
        fill: 'rgba(112, 4, 244, 0.2)'
    },
    blue_alpha: {
        border: 'rgba(151,187,205, 1)',
        fill: 'rgba(151,187,205,0.5)',
    },
    light_blue_alpha: {
        border: 'rgba(157, 249, 234, 1)',
        fill: 'rgba(157, 249, 234, 0.2)'
    },
    brown: {
        border: 'rgba(122, 63, 1)',
        fill: 'rgba(122, 63, 0.5)'
    },
    orange: {
        border: 'rgba(215, 84, 0, 0.9)',
        fill: 'rgba(215, 84, 0, 0.5)'
    },
    light_orange: {
        border: 'rgba(232, 138, 16, 1)',
        fill: 'rgba(232, 138, 16, 0.2)'
    },
    yellow: {
        border: 'rgba(229, 237, 7, 1)',
        fill: 'rgba(229, 237, 7, 0.2)'
    },
    gray: {
        border: 'rgba(168, 163, 163, 1)', 
        fill: 'rgba(168, 163, 163, 0.2)'
    },
    cyan: {
        border: 'rgba(27,187,225,0.9)',
        fill: 'rgba(27,187,225,0.5)'
    }
};

function setTicks(beginAtZero, stepSize, suggestedMax, max, min, reverse) {
    var ticks = {
        beginAtZero: beginAtZero,
        reverse: reverse,
        stepSize: stepSize,
        suggestedMax: suggestedMax,
        max: max,
        min: min,        
    };
    return ticks;
}

function configAxes(simple, type, display, position, id, gridlines, ticks, stacked) {
    if (simple) {
         var axes = {
            display: display,
            gridLines: {
                display: gridlines
            },
            stacked: stacked,
        };  
    }
    else {
        var axes = {
            type: type,
            display: display,
            position: position,
            id: id,
            gridLines: {
                display: gridlines,
            },
            ticks: ticks,
            stacked: stacked,
        };
    }
    return axes;
}

function chartConfig(type, data, scales, fill_line) {
    var config = {
        type: type,
        data: data,
        options: {
            responsive: true,
            legendTemplate: "lol",
            tooltips: {
                mode: 'label',
            },
            /*tooltips: {
                mode: 'label',
            },*/
            elements: {
                line: {
                    fill: fill_line,
                }
            },
            scales: scales,
        }
    }
    return config;
}

function round(num, bound=1){
    if(num % bound == 0)
        return num;

    return Math.ceil(num/bound)*bound;
}

function calculate_max(values, error=false) {
    var max = [];

    if (error) {
        for (i = 0; i < values.length; i += 2) {
           var max_temp = Math.max.apply(null, values[i]);
           var max_temp2 = Math.max.apply(null, values[i+1]);
           final_max = Math.ceil(max_temp + max_temp2);

           if (final_max <= 1) {
               max.push({max: 1, stepSize: 0.1});
           }
           else if (final_max < 10) {
               max.push({max: final_max, stepSize: 1});
           }
           else {
               max.push({max: final_max, stepSize: Math.ceil(final_max / 10)});
           }
        }
        return max; 
    }
    for (var v in values) {
        var max_temp = Math.max.apply(null, values[v]);
        max_temp = Math.ceil(max_temp);
        if (max_temp <= 1) {
            max.push({max:1, stepSize: 0.1});
        }
        else if (max_temp < 10) {
            max.push({max: max_temp, stepSize: 1});
        }
        else {
            max_temp = Math.ceil(max > max_temp ? max : max_temp)
            max.push({max: max_temp, stepSize: Math.ceil(max_temp / 10)});
        }
    }
    return max;
}

function new_setDataset(type, textLabel, color) {
    var dataset = {
        type: type,
        label: textLabel,
        borderColor: colors[color].border,
        backgroundColor: colors[color].fill,
        hoverBackgroundColor: colors[color].border,
        hoverBorderColor: colors[color].border,
        pointBorderColor: colors[color].border,
        pointBackgroundColor: colors[color].border,
        pointHoverBackgroundColor: colors[color].border,
        pointHoverBorderColor: colors[color].border,
        borderWidth: 3,
    }
    return dataset;
}

function create_data_object(data) {
    var datasets = {
        labels: [],
        values: []
    };
    
    for (var item in data) {
        datasets.labels.push(data[item][0]);
        if (data[item][1].length > 1) {
            for (var d in data[item][1]) {
                if (datasets.values.length <= d) {
                    datasets.values.push([]);
                }
                datasets.values[d].push(data[item][1][d]);
            }
        }
        else if (typeof data[item][1] == "object") {
            var object_key = Object.keys(data[item][1]);
            for (key in object_key) {
                if (datasets.values.length <= key) {
                    datasets.values.push([]);
                }
                datasets.values[key].push(data[item][1][object_key[key]]);
            }
        }
        else {
            if (datasets.values.length == 0) {
                datasets.values.push([]);
            }
            datasets.values[0].push(data[item][1]);
        }
    }
    return datasets;
}

function define_datasets(data, type, label, chosen_colors, error=false) {
    var obj = {
        datasets: []
    };
    if (error) {
        for (i = 0, j = 0; i < data.values.length; i += 2, j++) {
            obj.datasets.push(new_setDataset(type[i], label[j], chosen_colors[i]));
            obj.datasets[j].data = data.values[i];
            obj.datasets[j].error = data.values[i+1];
            obj.datasets[j].errorColor = colors[chosen_colors[i+1]].border;
        }
    }
    else {
        for (d in data.values) {
            obj.datasets.push(new_setDataset(type[d], label[d], chosen_colors[d]));
            obj.datasets[d].data = data.values[d];
        }
    }
    obj.labels = data.labels;
    
    return obj;
}

function define_scales(maxes) {
    var ticks = []
    var left = true;
    for (m in maxes) {
        ticks.push(setTicks(true, maxes[m].stepSize, maxes[m].max, maxes[m].max, 0));
    }
    var scales = {
        xAxes: [configAxes(true, null, true, null, null, true, null, true)],
        yAxes: [],
    };
    for (t in ticks) {
        if (left)
            scales.yAxes.push(configAxes(false, 'linear', true, 'left', null, true, ticks[t], true));
        else
            scales.yAxes.push(configAxes(false, 'linear', true, 'right', null, true, ticks[t], true));
        left = !left;
    }
    return scales;
}

function personalized_config(options, config) {
    var object_key = Object.keys(options);
    for (key in object_key) {
        switch (object_key[key]) {
            case 'reverse':
                yAxes = config.options.scales.yAxes;
                for (y in yAxes) {
                    yAxes[y].ticks.reverse = options['reverse'];
                }
                break;
            case 'fill':
                config.options.elements.line.fill = options['fill'];
                break;
            case 'stacked':
                /*yAxes = config.options.scales.yAxes
                for (y in yAxes) {
                    yAxes[y].stacked = options['stacked'];
                }*/
                nok = Object.keys(options[object_key[key]]);
                stacked = options['stacked'];
                for (nk in nok) {
                    if (typeof config.options.scales[nok[nk]] == 'object') {
                        scales = config.options.scales[nok[nk]];
                        for (s in scales) {
                            scales[s].stacked = stacked[nok[nk]];
                        }
                    }
                    else {
                        config.options.scales[nok[nk]].stacked = stacked[nok[nk]];
                    }
                }
                break;
            case 'yAxes':
                config.options.scales.yAxes = options['yAxes'];
                break;
            case 'yAxisID':
                datasets = config.data.datasets;
                for (d in datasets) {
                    datasets[d].yAxisID = options['yAxisID'][d];
                    config.options.scales.yAxes[d].id = options['yAxisID'][d];
                }
                break;
            case 'updateMax':
                yAxes = config.options.scales.yAxes;
                new_object_key = Object.keys(options[object_key[key]]);
                update_max = options['updateMax'];
                for (new_key in new_object_key) {
                    for (y in yAxes) {
                        if (yAxes[y].id == new_object_key[new_key]) {
                            yAxes[y].ticks.max = update_max[new_object_key[new_key]];
                            yAxes[y].ticks.suggestedMax = update_max[new_object_key[new_key]];
                        }
                    }
                }
                break;
            case 'displayGridlines':
                yAxes = config.options.scales.yAxes;
                new_object_key = Object.keys(options[object_key[key]]);
                display = options['displayGridlines'];
                for (new_key in new_object_key) {
                    for (y in yAxes) {
                        if (yAxes[y].id == new_object_key[new_key]) {
                            yAxes[y].gridLines.display = display[new_object_key[new_key]];
                        }
                    }
                }
                break;
            case 'yAxesDisplay':
                yAxes = config.options.scales.yAxes;
                new_object_key = Object.keys(options[object_key[key]]);
                display = options['yAxesDisplay'];
                for (new_key in new_object_key) {
                    for (y in yAxes) {
                         if (yAxes[y].id == new_object_key[new_key]) {
                             yAxes[y].display = display[new_object_key[new_key]];
                         }
                    }
                }
                break;             
            case 'yAxesPosition':
                yAxes = config.options.scales.yAxes;
                new_object_key = Object.keys(options[object_key[key]]);
                position = options['yAxesPosition'];
                for (new_key in new_object_key) {
                    for (y in yAxes) { 
                         if (yAxes[y].id == new_object_key[new_key]) {
                             yAxes[y].position = position[new_object_key[new_key]];
                         }
                    }
                }
                break;
            case 'maxAll':
                yAxes = config.options.scales.yAxes;
                maxAll = 0;
                for (y in yAxes) {
                     if (yAxes[y].ticks.max > maxAll) {
                         maxAll = yAxes[y].ticks.max;
                     }
                }
                for (y in yAxes) {
                     yAxes[y].ticks.max = maxAll;
                     yAxes[y].ticks.suggestedMax = maxAll;
                }
                break;
            case 'stepSizeAll':
                yAxes = config.options.scales.yAxes;
                stepSize = options['stepSizeAll'];
                for (y in yAxes) {
                    yAxes[y].ticks.stepSize = stepSize;
                }
                break;
            case 'tooltipCallbackLabel':
                tooltip_text = options["tooltipCallbackLabel"]["text"];
                config.options.tooltips['callbacks'] = {'label': null};
                config.options.tooltips.callbacks.title = function(tooltipItem, data) {
                return 'Cursada ' + tooltipItem[0].xLabel + ' vez(es)';
};
                config.options.tooltips.callbacks.label = function(tooltipItem, data) {
                    label = data.datasets[tooltipItem.datasetIndex].label;
                    if (options['tooltipCallbackLabel']['fixed']) {
                        value = tooltipItem.yLabel.toFixed(3);
                    }
                    else {
                        value = tooltipItem.yLabel;
                    }
                    if (options['tooltipCallbackLabel']['error']) {
                        error = data.datasets[tooltipItem.datasetIndex].error[tooltipItem.index].toFixed(3);;
                        return ''+ label + ': ' + value + unescape(tooltip_text) + error;
                    }
                    return '' + label + ": " + value + tooltip_text;
};
                break;
            default:
                // code
        }
    }
}

function build_line_chart(ctx, chart, colors=['blue_alpha', 'cyan', 'purple', 'grey']) {
    var data = create_data_object(chart.data);
    var the_data = define_datasets(data, ['line'], chart.labels, colors);
    var scales = define_scales(calculate_max(data.values));
    var chart_config = chartConfig('line',the_data, scales, true)

    if (chart.hasOwnProperty("options")) {
        personalized_config(chart.options, chart_config);
    }
    
    var chart = new Chart(ctx, chart_config);

    return chart;
}

function build_bar_chart(ctx, chart, colors=['blue_alpha', 'cyan']) {
    var data = create_data_object(chart.data);
    var the_data = define_datasets(data, ['bar', 'bar'], chart.labels, colors);
    var scales = define_scales(calculate_max(data.values));
    var chart_config = chartConfig('bar', the_data, scales, false);
    
    if (chart.hasOwnProperty("options")) {
        personalized_config(chart.options, chart_config);
    }
    
    var chart = new Chart(ctx, chart_config);

    return chart;
}

function build_line_bar_chart(ctx, chart, colors=['orange', 'blue_alpha']) {
    var data = create_data_object(chart.data);
    var the_data = define_datasets(data, ['line', 'bar'], chart.labels, colors);
    var scales = define_scales(data.values);
    var chart_config = chartConfig('bar', the_data, scales, false);

    if (chart.hasOwnProperty("options")) {
        personalized_config(chart.options, chart_config);
    }

    var chart = new Chart(ctx, chart_config);

    return chart;
}

function build_symmetric_error_line_chart(ctx, chart, colors=['blue_alpha', 'blue']) {
    var data = create_data_object(chart.data);
    var the_data = define_datasets(data, ['symmetricErrorLine'], chart.labels, colors, true);
    var scales = define_scales(calculate_max(data.values, true));
    var chart_config = chartConfig('symmetricErrorLine', the_data, scales, true);

    if (chart.hasOwnProperty("options")) {
        personalized_config(chart.options, chart_config);
    }

    var chart = new Chart(ctx, chart_config);

    return chart;
}

function build_symmetric_error_bar_chart(ctx, chart, colors=['orange', 'brown', 'blue_alpha', 'blue']) {
    var data = create_data_object(chart.data);
    var the_data = define_datasets(data, ['symmetricErrorBar'], chart.labels, colors, true);
    var scales = define_scales(calculate_max(data.values, true));
    var chart_config = chartConfig('symmetricErrorBar', the_data, scales, true);

    if (chart.hasOwnProperty("options")) {
        personalized_config(chart.options, chart_config);
    }
    var chart = new Chart(ctx, chart_config);
    return chart;
}
