class AdegaChart{

    constructor(config){
        
        //Object with two arrays (two charts), and the key is the x-axis
        this.data = config.data || null;

        if(config.data == null){
            this.data_x = config.data_x;
            this.data_y = config.data_y;
            this.error_y = config.error_y || null;
        }
        else{
            this.data_x = [];
            this.data_y = [[],[]];
            for(var obj in this.data){
                this.data_x.push(obj);
            }
            this.data_x.sort();
            for(var i in this.data_x){
                var key = this.data_x[i];
                this.data_y[0].push(this.data[key][0]);
                this.data_y[1].push(this.data[key][1]);
            }
        }

        this.fill = config.fill || "tozeroy";
        this.div_target = config.div_target;
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
        title: this.title
        };
        Plotly.newPlot(this.div_target, data, layout);
    }

}