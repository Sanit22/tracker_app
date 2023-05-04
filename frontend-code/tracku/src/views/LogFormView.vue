<template>
<div>
    <NavBar> </NavBar>
    <h1 class="mt-4 text-center text-decoration-underline"> {{ tracker_name }} </h1>
    <div class="d-flex">
    <div id="log-form-container" class="mx-auto bg-white border rounded mt-4">
    
        <h2 v-if="action === 'create'" class="mt-4 text-center text-decoration-underline p-4"> Create a log </h2>
        <h2 v-if="action === 'edit'" class="mt-4 text-center text-decoration-underline p-4"> Edit log </h2>


            <form class="d-flex flex-column align-items-center p-2 w-100 rounded mt-3" id="log-form" @submit.prevent="sendFormData"
            method="POST">
                <div class="d-flex justify-content-start align-items-center mb-3 w-100 p-3">
                    <label for="note"> Note: </label>
                    <input name="note" v-model="note" type="text" class="ms-4 p-2">
                </div>
    
            
                    
                <div v-if=" tracker_type === 'Numerical' || tracker_type === 'Time Duration'" class="d-flex justify-content-start align-items-center mb-3 w-100 p-3">
                    <label for="value"> Value: </label>
                    <input v-model="value" name="value" class="ms-3 p-2">
                    <span class="ms-3 fw-bold"> {{ tracker_settings[0] }}</span>
                </div>
            
                <div v-else class="d-flex justify-content-start align-items-center mb-3 w-100 p-3">
                        <label for="value"> Value: </label>
                        <select v-model="value" name="value" class="ms-3 p-2">
                            <option class="p-2" v-for="setting in tracker_settings" :key="setting">
                                    {{ setting }} 
                            </option>
                        </select>
                </div>
              
                <div class="d-flex justify-content-start align-items-center mb-3 w-100 p-3"  >
                    <label> When: </label>
                    <input v-model="timestamp" class="ms-3 p-2" id="datetime" name="timestamp" type="datetime-local">
                </div>
                <button class="btn btn-secondary" v-if="action === 'create'" type="submit"> Create log </button>
                <button v-if="action === 'edit'" type="submit"> Edit log </button>
            </form>
        </div>
        </div>
</div>
    
</template>

<script>
import NavBar from '../components/NavBar.vue';
import Vue from 'vue'

export default({
    name:'LogFormView',
    components:{
        NavBar,
    },
    data(){
        return{
            tracker_id:this.$route.params.tracker_id,
            log_id:'',
            action: this.$route.params.action,
            tracker_name:'',
            tracker_type:'',
            tracker_settings:[],
            timestamp:'',
            note:'',
            value: '',
        }
    },
    computed:{
        
    },
    beforeMount(){
        if(this.action === 'create'){
            this.createLogForm()
        }
        else{
            this.editLogForm()
        }
    },
    methods:{
        currentDateTime: function(){
            let today = new Date();

            // YYYY-MM-DDThh:mm
            let datestring = today.getFullYear() + '-' + ('0' + (today.getMonth() + 1)).slice(-2) + '-'
             + ('0' + today.getDate()).slice(-2) + 'T' + ('0' + today.getHours()).slice(-2) + ':' + ('0' + today.getMinutes()).slice(-2)
             this.timestamp = datestring;
        },
        createLogForm: async function(){
            // let access_token = localStorage.getItem('access_token');
            const response = await fetch('http://localhost:8000/api/create_log_form?tracker_id='+this.tracker_id+'',{
                credentials: 'include',
            })
            .then((response) => {
                if(response.status === 400){
                    this.$router.push('/error')
                }
                return response.json()
            })
            .then((data) => {
                console.log(data)
                this.tracker_name = data.tracker_name
                this.tracker_type = data.tracker_type
                this.tracker_settings = data.tracker_settings
                if(this.tracker_type == "Multiple Choice" || this.tracker_type == "Boolean")
                    this.value = data.tracker_settings[0]
                this.currentDateTime();
                
                })
            .catch((err) => console.log(err))
        },
        sendFormData: async function(){
            let log_form = document.getElementById("log-form");
            let form_data = new FormData(log_form)
            if(this.action === 'create'){
                const response = await fetch('http://localhost:8000/api/add_log?tracker_id='+this.tracker_id+'',{
                method: 'POST',
                credentials: 'include',
                body: form_data,
            })
            .then((response) => {
                if(response.status === 400){
                    Vue.notify({
                        group: 'foo',
                        type: 'error',
                        title: 'Something went wrong!',
                        text: 'Unable to add log. Please check and submit again.'
                    });
                    window.location.reload()
                }
                return response.json()
            })
            .then((data) => {
                console.log(data)
                
                    Vue.notify({
                        group: 'foo',
                        type: 'success',
                        title: 'Log added!',
                        text: 'Successfully added log!'
                    });
                    this.$router.push({ path: '/view_logs/'+this.tracker_id+''})
                
            })
            }
            else if(this.action === 'edit'){
                const response = await fetch('http://localhost:8000/api/edit_log?tracker_id='+this.tracker_id+'&log_id='+this.log_id+'',{
                    method: 'POST',
                    credentials: 'include',
                    body: form_data,
                })
                .then((response) => {
                    if(response.status === 400){
                    Vue.notify({
                        group: 'foo',
                        type: 'error',
                        title: 'Something went wrong!',
                        text: 'Unable to edit log. Please check and submit again.'
                    });
                    window.location.reload()
                    }
                })
                .then((data) => {
                   
                    Vue.notify({
                        group: 'foo',
                        type: 'success',
                        title: 'Log edited!',
                        text: 'Successfully edited log!'
                    });
                    this.$router.push({ path: '/view_logs/'+this.tracker_id+''})
                    console.log(data)})
            }
        },
        editLogForm: async function(){
            this.log_id = this.$route.params.log_id
            const response = await fetch('http://localhost:8000/api/edit_log_form?tracker_id='+this.tracker_id+'&log_id='+this.log_id+'',{
                credentials: 'include',
            })
            .then((response) => {
                if(response.status === 400){
                    this.$router.push('/error')
                }
                return response.json()
            })
            .then((data) => {
                console.log(data)
                let log_info = data.log_data
                this.log_id = log_info.log_id
                this.timestamp = log_info.timestamp
                this.value = log_info.value
                this.tracker_settings = data.tracker_settings
                this.note = log_info.note
                this.tracker_type = data.tracker_type
                this.tracker_name = data.tracker_name
            })
        }
    }
})


</script>

<style scoped>
#log-form-container{
    width:400px;
    height:500px;
}

</style>