<template>
    <div>
    <div class="card ms-3 tracker-card mt-2" style="width: 15rem; height: 15rem;">
        <p id="tracker_name" class="mt-3 mx-auto w-75 border bg-secondary rounded fs-2 text-center fw-light text-white"> {{ tracker_name }} </p> 
        <div class="dropdown mt-2">
            <button class="btn dropdown-toggle options_button" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
            Options
            </button>
            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                <li>
                    <router-link class="dropdown-item" :to="{ name: 'log_form', params: { tracker_id: tracker_id, action: 'create' } }">  Create log </router-link>
                </li>
                <li>
                    <router-link class="dropdown-item" :to="{ name: 'view_logs', params: { tracker_id } }"> View logs </router-link>
                </li>
                <li>
                    <router-link class="dropdown-item" :to="{ name: 'tracker_form', params: { action: 'edit', tracker_id : tracker_id} }"> Edit tracker </router-link>
                </li>
                <li>
                    <a class="dropdown-item" href="" @click="deleteTracker(tracker_id)"> Delete Tracker </a>
                </li>
            </ul>
            <p class="mt-4 fw-bold fst-italic"> <span class="text-decoration-underline fw-bolder">Last logged:</span> {{ last_logged }} </p>
        </div> 



        <!-- <div class="card m-3" style="width: 15rem; height: 15rem;">
                <div class="card-body">
                    <h5 class="card-title">{{ tracker_name }}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">{{ tracker_type }}</h6>
                    
                    <!-- <a href="#" class="card-link">Card link</a>
                    <a href="#" class="card-link">Another link</a> -->
                    <!-- <div class="dropdown">
                        <button class="btn dropdown-toggle options_button" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                        Options
                        </button>
                    <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                        <li>
                            <router-link class="dropdown-item" :to="{ name: 'log_form', params: { tracker_id: tracker_id, action: 'create' } }">  Create log </router-link>
                        </li>
                        <li>
                            <router-link class="dropdown-item" :to="{ name: 'view_logs', params: { tracker_id } }"> View logs </router-link>
                        </li>
                        <li>
                            <router-link class="dropdown-item" :to="{ name: 'tracker_form', params: { action: 'edit', tracker_id : tracker_id} }"> Edit tracker </router-link>
                        </li>
                        <li>
                            <a class="dropdown-item" href="" @click="deleteTracker(tracker_id)"> Delete Tracker </a>
                        </li>
                    </ul>
                    <p class="card-text">Last logged: {{ last_logged }}</p>
                    </div>
                </div> --> 
        </div>
    </div>

</template>


<script>
import Vue from 'vue'
export default {
    name: 'TrackerInfo',
    props: ['tracker_id', 'tracker_name', 'last_logged'],
    methods:{
        deleteTracker: async function(tracker_id){
            const response = await fetch('http://localhost:8000/api/delete_tracker?tracker_id='+tracker_id+'',{
                credentials:'include'
            }) 
            .then((response) => {
                if(response.status === 400){
                    Vue.notify({
                        group: 'foo',
                        type: 'error',
                        title: 'Something went wrong!',
                        text: 'Unable to delete tracker. Please try again.'
                    });
                    window.location.reload()
                }
                return response.json()
            })
            .then((data) => {
                Vue.notify({
                    group: 'foo',
                    type: 'sucess',
                    title: 'Tracker deleted successfully!',
                    text: 'Tracker deleted successfully.'
                });
                console.log(data)

            })
        }
    }
}

</script>

<style scoped>
    .options_button{
        background-color: rgb(79, 79, 252);
        color:white;
    }
</style>
