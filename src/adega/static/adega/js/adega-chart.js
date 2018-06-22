class AdegaChart{

    constructor(config){
        this.data = null;
        this.data_x = config.data_x;
        this.data_y = config.data_y;
        this.div_target = config.div_target;
        this.error_y = config. error_y || null;
        this.type = config.type || "scatter";
        this.title = config.title || "";
        this.legend = config.legend || null;

        if(typeof(this.data_y[0]) == "number"){
        this.data_y = [this.data_y];
        this.type = [this.type];
        this.legend = [this.legend];
        if(this.error_y != null)
            this.error_y = [this.error_y];
        
        }

        this.reloadGraph();
    }

    reloadGraph(){
        var data = [];

        for(var i in this.data_y){
        data.push(
            {
            x: this.data_x,
            y: this.data_y[i],
            type: this.type[i],
            fill: "tozeroy"
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
        title: this.title
        };
        Plotly.newPlot(this.div_target, data, layout);
    }

}