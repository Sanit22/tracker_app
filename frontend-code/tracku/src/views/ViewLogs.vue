<template>
<div id="main-div">
    <NavBar> </NavBar>
    <div class="d-flex">
    <div class="mx-auto mt-3 bg-white w-75 p-4 ms-4" id="main-container">   
        <h2 class="text-decoration-underline mt-3"> {{ tracker_name }}</h2>

        <DoughnutChart 
        v-if="tracker_type == 'Boolean' || tracker_type == 'Multiple Choice'"
        v-bind:chartData="chartData"
        />
        <BarChart
        v-else
        v-bind:chartData="chartData"/>

        <table class="table p-3 w-100 table-bordered  mt-4">
            <thead>
                <tr>
                <th> Note </th>
                <th> Value </th>
                <th> Timestamp </th>
                <th> Settings </th>
                </tr>
            </thead>
            <!-- <tr>
                <th> Note </th>
                <th> Value </th>
                <th> Timestamp </th>
                <th> Settings </th>
            </tr> -->
            <tbody>
            
            <tr v-for="log in logs" :key="log.log_id">
                <td> {{ log.note }} </td>
            
                <td> {{ log.value }} </td>
            
                <td> {{ log.timestamp}} </td>    
                <td>           
                    <div class="dropdown">
                        <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                            Options
                        </button>
                        <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                            <li>
                                <router-link :to="{ name: 'log_form', params: { 'tracker_id': tracker_id, 'log_id': log.log_id, 'action': 'edit' } }" class="dropdown-item"> Edit log </router-link>
                            </li>
                            <li><a v-on:click="deleteLog(log.log_id)" class="dropdown-item" href="">Delete log</a></li>
                        </ul>
                    </div>
                </td>
            </tr>
            </tbody>
        </table>
        
    </div>

    <div id="extra_options" class="mt-4 p-3 ms-2 me-4">
        <h3 class="text-decoration-underline"> Options</h3>
        <div class="d-flex justify-content-center flex-wrap mt-3 mb-3" id="export_logs">
          <p> Export logs as csv:  </p>
          <button class="btn btn-outline-secondary mt-2" id="export_button" @click="exportLogs"> Export Logs </button>
          <button class="ms-2 btn btn-outline-secondary mt-2" @click = "downloadLogs" id="download_button"> Download </button>
        </div>  
        <router-link class="link-secondary fs-5 mt-4" :to="{ name: 'log_form', params: { tracker_id: tracker_id, action: 'create' } }">  Create log </router-link>
    </div>
    </div>
</div>
    
</template>


<script>
import NavBar from '../components/NavBar.vue';
import axios from 'axios'
import Vue from 'vue'
import DoughnutChart from '../components/DoughnutChart.vue'
import BarChart from '../components/BarChart.vue'


    export default{
        name:'ViewLogs',
        components:{
            NavBar,
            DoughnutChart,
            BarChart,
        },
        data(){
            return{
                user_name:'user',
                log_id:'',
                note:'',
                value:'',
                timestamp:'',
                tracker_id:this.$route.params.tracker_id,
                logs:[],
                tracker_name:'',
                tracker_type:'',
                chart_labels:[],
                chart_data:[],
                chartData:{},
            }
        },
        mounted(){
        
            let download = document.getElementById("download_button");
            download.style.display = "none";
            this.fetchLogData()

           
            const response = fetch('http://localhost:8000/api/getchartdata?tracker_id='+this.tracker_id+'',{
                credentials: 'include'
            })
            .then((response) => {
                if(response.status === 400){
                    this.$router.push('/error')
                }
                return response.json()
            })
            .then((data) => {
                console.log(data);

                if(this.tracker_type === "Numerical" || this.tracker_type === "Time Duration"){
                    this.chart_labels = data.labels_nt     
                }
                else{
                    this.chart_labels = data.labels_mb
                    
                }
                for(let label of this.chart_labels){
                        this.chart_data.push(data.data_dict[label])
                }
                console.log(this.chart_labels)
                console.log(this.chart_data)

                let bg_colour = []
                let base = null;
                let bd_colour = []

                if(this.tracker_type === "Multiple Choice"){
                    bg_colour = ['#41B883', '#E46651', '#00D8FF', '#DD1B16']
                }
                else if(this.tracker_type === "Boolean"){
                    bg_colour = ['#41B883', '#E46651']
                }
                else{
                    bg_colour = ['rgba(255, 99, 132, 0.2)',
                                'rgba(255, 159, 64, 0.2)',
                                'rgba(255, 205, 86, 0.2)',
                                'rgba(75, 192, 192, 0.2)',
                                'rgba(54, 162, 235, 0.2)',
                                'rgba(153, 102, 255, 0.2)',
                                'rgba(201, 203, 207, 0.2)']
                    bd_colour: [
                                'rgb(255, 99, 132)',
                                'rgb(255, 159, 64)',
                                'rgb(255, 205, 86)',
                                'rgb(75, 192, 192)',
                                'rgb(54, 162, 235)',
                                'rgb(153, 102, 255)',
                                'rgb(201, 203, 207)'
                                ]
                }


                this.chartData = {
                    labels: this.chart_labels,
                    datasets: [ 
                        {
                            label: 'Visualise your progress',
                            backgroundColor: bg_colour,
                            borderColor: bd_colour,
                            data: this.chart_data,
                            borderWidth: 1,
                        }],
                }
                console.log(this.chartData)
            })
        },
        methods:{
            fetchLogData: async function(){
                const response = await fetch('http://localhost:8000/api/view_logs?tracker_id='+ this.tracker_id +'',
                {
                    credentials: 'include'
                }).then((response) => {
                    if(response.status === 400){
                        this.$router.push('/error')
                    }
                    return response.json()
                })
                .then((data) => {
                    console.log(data)
                    this.user_name = data.user_name
                    this.logs = data.logs
                    this.tracker_name = data.tracker_name
                    this.tracker_type = data.tracker_type
                })
            },
            deleteLog: async function(log_id){
                const response = await fetch('http://localhost:8000/api/delete_log?log_id='+log_id+'',{
                    credentials: 'include'
                }).then((response) => {
                    if(response.status === 400){
                        Vue.notify({
                        group: 'foo',
                        type: 'error',
                        title: 'Something went wrong!',
                        text: 'Error while deleting the log.'
                    });
                        window.location.reload()
                    }
                    return response.json()
                })
                .then((data) =>{
                    Vue.notify({
                        group: 'foo',
                        type: 'success',
                        title: 'Log deleted!',
                        text: 'Successfully deleted log.'
                    });
                    console.log(data)
                }) 
            },
            createLogForm: function(){
                this.$router.push('/log_form/'+this.tracker_id+'/create')
            },
            exportLogs: function(){
                var source = new EventSource("http://localhost:8000/api/export_logs", { withCredentials: true });
                source.addEventListener('message', function(event) {
                    console.log("Successfully received stream ** ** **")
                    let data = event.data
                    console.log(data)
                    if(data === "csv created "){
                        Vue.notify({
                            group: 'foo',
                            type: 'success',
                            title: 'Download ready!',
                            text: 'Your logs are ready to download!'
                        });
                        let download = document.getElementById("download_button");
                        download.style.display = "block";
                    }
                    else{
                        console.log("csv not created yet!")
                    }
                    
                }, false);
                source.addEventListener('error', function(event) {
                    source.close()
                }, false);
            },
            downloadLogs: function(){
                axios({
                    url: 'http://localhost:8000/api/download_logs', 
                    method: 'GET',
                    responseType: 'blob',
                    withCredentials: true
                    }).then((response) => {
                        console.log(response)
                        console.log(typeof(response.data))
                        // var FILE = window.URL.createObjectURL(new Blob([res.data]));
                        const FILE = new Blob([response.data], { type: 'application/csv' })
                        // const FILE = URL.createObjectURL(res.data);
                        const link = document.createElement('a');
                        link.href = URL.createObjectURL(FILE);
                        let filename = ''+this.user_name+'_logs.csv'
                        link.setAttribute('download', filename);
                        document.body.appendChild(link);
                        link.click();
                        URL.revokeObjectURL(link.href)
                        }).catch((err) => {
                        console.error(err)
                        })
                }
        }
    }

</script>

<style scoped>
#main-div{
    height: 100%;
}

#main-container{
    margin-left:15%;
}

#extra_options{
    width:250px;
    background-color:rgb(217, 217, 217);
    height: 280px;
}

</style>