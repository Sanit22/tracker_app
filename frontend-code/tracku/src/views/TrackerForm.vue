<template>
    <div id="main-div" class="h-100">
        <NavBar> </NavBar>
        <h1 v-if="action === 'create'" class="mt-4 text-center text-decoration-underline"> Create Tracker </h1>
        <h1 v-if="action === 'edit'" class="mt-4 text-center text-decoration-underline"> Edit Tracker </h1>
    <div id="tracker-form-container" class="bg-white p-2 mx-auto mt-4">
        
        <form @submit.prevent="sendFormData" id="tracker-form" class="d-flex flex-column align-items-center p-2 w-100 rounded" method="POST">
                <div class="mb-3 w-100">
                    <label for="tracker_name" class="form-label"> Name: </label>
                    <input name="tracker_name" class="ms-3 p-2" type="text" v-model="tracker_name">
                </div>
                <div class="mb-3 w-100">
                    <label for="tracker_type" class="form-label"> Tracker Type: </label>
                    <select @change="clearSettings" class="ms-3 p-2" name="tracker_type" v-model="tracker_type" >
                        <option class="p-2" v-for="tracker in tracker_list" :key="tracker"> {{ tracker }} </option>
                    </select>
                </div>
                <div  class="mb-3 w-100">
                    <label for="description" class="form-label"> Description: </label>
                    <input name="description" class="ms-3 p-2" type="text" v-model="description">
                </div>
                <div class="mb-3 w-100" id="settings">
                    <h4 class="text-decoration-underline mb-2"> Settings </h4>
                    <div v-if="tracker_type === 'Time Duration'">
                        <label for="settings"> Set time unit: </label>
                        <select name="settings" class="ms-3 p-2" v-model="time_duration_set">
                            <option class="p-2" v-for="option in time_options" :key="option"> {{ option }} </option>
                        </select>
                    </div>
                    <div v-if="tracker_type === 'Boolean'">
                        <select disabled class="ms-3 p-2">
                            <option> Yes/No </option>
                            <option v-for="option in bool_options" :key="option"> {{ option }}  </option>
                        </select>
                    </div>
                    <div v-if="tracker_type === 'Numerical'">
                         <label for="settings"> Set unit: </label>
                         <input  class="ms-3 p-2" name="settings" placeholder="e.g. kms, laps, rounds" v-model="tracker_settings" type="text">
                    </div>
                    
                    <div v-if="tracker_type === 'Multiple Choice'">
                         <label for="settings"> Add options: </label>
                         <input class="ms-3 p-2" name="settings" placeholder="e.g. happy, sad, angry" v-model="tracker_settings" type="text">
                    </div>
                </div> 
                <button class="btn btn-secondary" v-if="action === 'create'" type="submit"> Add Tracker   </button> 
                <button class="btn btn-secondary" v-if="action === 'edit'" type="submit"> Edit Tracker   </button> 
            </form>
        </div>
    </div>
</template>

<script>
import NavBar from '../components/NavBar.vue'
import Vue from 'vue'

export default{
    name:"TrackerForm",
    components:{
        NavBar,
    },
    data(){
        return{
            tracker_id:'',
            action:this.$route.params.action,
            tracker_name:'',
            tracker_type:'Numerical',
            tracker_settings:'',
            description:'',
            tracker_list:['Numerical', 'Boolean', 'Time Duration', 'Multiple Choice'],
            time_options:['hours', 'minutes', 'seconds'],
            bool_options:['Yes', 'No'],
            time_duration_set:'hours',
        }
    },
    beforeMount(){
        if(this.action === 'create'){
            if(!session['user_id']){
                this.$router.push('/error')
            }
        }
        if(this.action === 'edit'){
            this.fetchFormData()
        }
    },
    methods:{
        fetchFormData: async function(){
            this.tracker_id = this.$route.params.tracker_id
            const response = await fetch('http://localhost:8000/api/edit_tracker_form?tracker_id='+this.tracker_id+'',{
                credentials:'include'
            })
            .then((response) => {
                if(response.status === 400){
                    this.$router.push('/error')
                }
                return response.json()
            })
            .then((data) => {
               
                let tracker = data.tracker_details
                this.tracker_name = tracker.tracker_name
                this.description = tracker.description
                this.tracker_type = tracker.tracker_type
                let settings = tracker.tracker_settings
                let tracker_settings = ''
                for (let setting of settings){
                    tracker_settings += setting + ','
                }
                tracker_settings = tracker_settings.slice(0, -1)
                this.tracker_settings = tracker_settings
                if(this.tracker_type === 'Time Duration'){
                    this.time_duration_set = tracker_settings
                }
                    
            })
        },
        sendFormData: async function(){
            let tracker_form = document.getElementById("tracker-form")
            let form_data = new FormData(tracker_form)
            if(this.action === 'create'){
                const response = await fetch('http://localhost:8000/api/create_tracker',{
                method:'POST',
                credentials:'include',
                body: form_data
            })
            .then((response) => {
                if(response.status === 400){
                    Vue.notify({
                        group: 'foo',
                        type: 'error',
                        title: 'Something went wrong!',
                        text: 'Unable to add tracker. Please check and submit again.'
                    });
                    this.$router.push('/error')
                }
                return response.json()
                })
            .then((data) => {
                console.log(data)
                Vue.notify({
                    group: 'foo',
                    type: 'success',
                    title: 'Tracker created!',
                    text: 'Successfully added tracker!'
                });
                this.$router.replace({ path: '/dashboard' })
        
                
            })
            }
            if(this.action === 'edit'){
                const response = await fetch('http://localhost:8000/api/edit_tracker?tracker_id='+this.tracker_id+'',{
                method:'POST',
                credentials:'include',
                body: form_data
            })
            .then((response) => {
                console.log(response)
                if(response.status === 400){    
                    Vue.notify({
                        group: 'foo',
                        type: 'error',
                        title: 'Something went wrong!',
                        text: 'Unable to edit tracker. Please check and submit again.'
                    });
                    this.$router.push('/error')
                }
                return response.json()
                })
            .then((data) => {
                console.log(data);
                Vue.notify({
                    group: 'foo',
                    type: 'success',
                    title: 'Tracker edited!',
                    text: 'Successfully edited tracker!'
                });
                this.$router.replace({ path: '/dashboard' })

                
                
            })
            }
        },
        clearSettings: function(){
            this.tracker_settings = ''
        }
    }
}
</script>

<style scoped>
#tracker-form-container{
    height:400px;
    width: 400px;
}
</style>