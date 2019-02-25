// This module simplify the use of Plotly library on this project

class AdegaChart{

    constructor(config){
        
        //Object with two arrays (two charts), and the key is the x-axis
        this.data = config.data || null;
        
        this.hide_charts = config.hide_charts || null;
        
        this.legend = config.legend || null;

        this.barmode = config.barmode || "stack";
        
        this.yaxis_title = config.yaxis_title || "";
        this.yaxis2_title = config.yaxis2_title || "";
        this.xaxis_title = config.xaxis_title || "";
        
        this.mode = config.mode;
        
        this.marker = config.marker;

        if(config.data == null){
            this.data_x = config.data_x;
            this.data_y = config.data_y;
            this.error_y = config.error_y || null;
        }
        else{
            this.data_x = [];
            this.data_y = [];
            var first_element = Object.keys(this.data)[0];

            first_element = this.data[first_element];
            var multiplePlots = Array.isArray(first_element);

            if(multiplePlots){
                for(var i in first_element){
                    this.data_y.push([]);
                }
            }

            for(var obj in this.data){
                this.data_x.push(obj);
            }
            this.data_x.sort();
            for(var i in this.data_x){
                var key = this.data_x[i];

                if(multiplePlots){
                    for(var i in first_element){
                        this.data_y[i].push(this.data[key][i]);
                    }
                }
                else{
                    this.data_y.push(this.data[key]);
                }

            }
        }

        this.fill = config.fill || "tozeroy";
        this.div_target = config.div_target;
        this.type = config.type || "scatter";
        this.title = config.title || "";
        
        
        if(typeof(this.data_y[0]) == "number"){
            this.data_y = [this.data_y];
            this.type = [this.type];
            this.legend = [this.legend];
            
            if(this.error_y != null)
                this.error_y = [this.error_y];
        }


        this.data_axis_y = config.data_axis_y || this.data_y.map(function(x){return "y1";});

        this.reloadGraph();
    }

    transformToAcumulation(){
        var number_lines = this.data_y.length;

        for(var i in this.data_y){
            var acumulation = 0;
            for(var j in this.data_y[i]){
                acumulation += this.data_y[i][j];
                this.data_y[i][j] = acumulation;
            }
        };
        this.reloadGraph();
    }

    reloadGraph(){
        var data = [];
        for(var i in this.data_y){
            if(this.hide_charts && this.hide_charts[i])
                continue;
            data.push(
                {
                    x: this.data_x,
                    y: this.data_y[i],
                    type: this.type[i],
                    fill: this.fill,
                    yaxis: this.data_axis_y[i],
                }
            );
            
            if(this.legend && this.legend[i] != null){
                data[i].name = this.legend[i];
            }

            if(this.error_y && this.error_y[i] != null){
                data[i].error_y = {
                    type: 'data',
                    array: this.error_y[i],
                    visible: true,
                }
            }
            if(this.mode && this.mode[i]){
                data[i].mode = this.mode[i];
            }
            if(this.marker != undefined){
                data[i].marker = this.marker;
            }
        }

        var layout = {
            title: this.title,
            showlegend: true,
            xaxis:{
                title:this.xaxis_title
            },
            yaxis: {
                title: this.yaxis_title,
                rangemode: 'tozero'
                // overlaying: 'y'
            },
            yaxis2: {
                // title: 'yaxis2 title',
                // titlefont: {color: 'rgb(148, 103, 189)'},
                // tickfont: {color: 'rgb(148, 103, 189)'},
                overlaying: 'y1',
                side: 'right',
                rangemode: 'tozero',
                title: this.yaxis2_title,
            },
            barmode: this.barmode
        };
        
        Plotly.newPlot(this.div_target, data, layout);
    }

}

AdegaChart.sort_object_by_key = function(obj){
    keys = Object.keys(obj);
    keys.sort();
    values = keys.map(function(x){
        return obj[x];
    });

    return [keys,values];
}