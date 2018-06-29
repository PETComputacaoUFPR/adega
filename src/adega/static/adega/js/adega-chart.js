class AdegaChart{

    constructor(config){
        
        //Object with two arrays (two charts), and the key is the x-axis
        this.data = config.data || null;
        
        this.hide_charts = config.hide_charts || null;
        
        this.legend = config.legend || null;


        if(config.data == null){
            this.data_x = config.data_x;
            this.data_y = config.data_y;
            this.error_y = config.error_y || null;
        }
        else{
            this.data_x = [];
            this.data_y = [];
            var first_element;
            for (first_element in this.data) break;
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
                fill: this.fill
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
        }

        var layout = {
            title: this.title,
            showlegend: true
        };
        Plotly.newPlot(this.div_target, data, layout);
    }

}