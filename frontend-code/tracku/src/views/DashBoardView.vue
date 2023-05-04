<template>
    <div id="main-div">
        <NavBar> </NavBar>
        
        <div class="d-flex h-100">
          
        <div id="main-container" class="bg-white p-4 w-75"> 
            <h2 class="mt-3 fs-1 text-decoration-underline"> My Trackers </h2>
            <div id="all-trackers " class="d-flex flex-wrap w-100">
              <TrackerInfo v-for="tracker in trackers"
              v-bind:key="tracker.tracker_id"
              v-bind:tracker_name="tracker.tracker_name"
              v-bind:tracker_type="tracker.tracker_type"
              v-bind:last_logged="tracker.last_logged"
              v-bind:tracker_id="tracker.tracker_id"
              >
              </TrackerInfo>
                
            </div>
            </div>
        <div>
            <!-- <ul v-for="tracker in tracker_dict" :key="tracker.id">
              <li> {{ tracker.name }}</li>
            </ul> -->
        </div>

        <div class="p-3 ms-2 mt-2 me-2" id="extra_options">
          <h3 class="text-decoration-underline"> Options </h3>
          <p class="mt-2"> Report format: </p>
          <div class="d-flex mt-3 justify-content-center"> 
          <div>
          <input class="ms-3" v-model="curr_format" type="radio" name="format" id="html" value="html">
          <label class="ms-1"> HTML </label>
          </div>
          <div>
          <input class="ms-3" v-model="curr_format" type="radio" name="format" id="pdf" value="pdf">
          <label class="ms-1"> PDF </label>
          </div>
        </div>

        <div class="d-flex justify-content-center flex-wrap mt-3" id="export_trackers">
          <button class="me-3 btn btn-outline-secondary" id="export_button" @click="exportTrackers"> Export Trackers </button>
          <button class="mt-2 btn btn-outline-secondary" @click = "downloadTrackers" id="download_button"> Download </button>
        </div>
        </div>
        </div>
    </div>
</template>



<script>
import NavBar from '../components/NavBar.vue';
import TrackerInfo from '../components/TrackerInfo.vue';
import axios from 'axios'
import Vue from 'vue'

export default {
  name: "DashBoardView",
  components:{
    NavBar,
    TrackerInfo,
  },
  data() {
    return{
        user_name: "user",
        trackers: [],
        curr_format:'html',
        tracker_list:[],
    }
  },
  beforeMount(){
    this.fetchUserData()
  },
  mounted(){
    let download = document.getElementById("download_button");
    download.style.display = "none";
},
  methods:{
    fetchUserData: async function(){
        // let access_token = localStorage.getItem('access_token');
        // console.log(access_token)
        const response = await fetch('http://localhost:8000/api/dashboard',{
            credentials: 'include',
        })
        .then((response) => {
          if(response.status == 401){
            throw new Error('Please login!')
          }
          return response.json()
        })
        .then((data) => {
          this.trackers = data.dashboard_data
          this.user_name = data.user_name
       
        }).catch((error) => {
          console.log(error)
          this.$router.push('/')
          })    
    },
    TrackerFormNavigate: function(){
      this.$router.push({ name: 'tracker_form', params: { action: 'create' } })
    },
    exportTrackers: function(){
    var source = new EventSource("http://localhost:8000/api/export_trackers", { withCredentials: true });
    source.addEventListener('message', function(event) {
        // var data = JSON.parse(event.data);
        console.log("Successfully received stream ** ** **")
        let data = event.data
        console.log(data)
        if(data === "csv created "){
          Vue.notify({
                group: 'foo',
                type: 'success',
                title: 'Download ready!',
                text: 'Your Trackers are ready to download!'
              });
          let download = document.getElementById("download_button");
          download.style.display = "block";
        }
        else{
          console.log("csv not created yet!")
          Vue.notify({
                group: 'foo',
                type: 'success',
                title: 'Something went wrong!',
                text: 'Unable to process request. Please try again.'
              });
        }
        
    }, false);
    source.addEventListener('error', function(event) {
        source.close()
    }, false);
  },
  downloadTrackers: function(){
    axios({
          url: 'http://localhost:8000/api/download_trackers', 
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
            let filename = ''+this.user_name+'_trackers.csv'
            link.setAttribute('download', filename);
            document.body.appendChild(link);
            link.click();
            URL.revokeObjectURL(link.href)
            }).catch((err) => {
              console.error(err)
            })
    }
  },
  watch:{
    curr_format: function(new_format){
      const response = fetch('http://localhost:8000/api/change_format?format='+new_format+'',{
            credentials: 'include',
      })
      .then((response) => response.json())
      .then((data) => console.log(data)) 
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
  height: 100%;
}



#extra_options{
  width:200px;
  background-color:rgb(217, 217, 217);
  height: 300px;
}

#all-trackers{
  margin-top: 50px;
}

.tracker-card{
    border-radius: 13px;
    margin-bottom:70px;
    background-color: rgb(245, 245, 245);
    padding: 15px;
    color: rgba(140, 140, 140, 0.833);
    height: 20vh;
    width: 20vw;
}




</style>