<template>
  <div class="home h-100 d-flex align-items-center justify-content-around flex-wrap">
    <div class="login_divs">
      <h1> TrackU</h1>
      <p> Track yourself and improve based on data </p>
    </div>
    <div class="login_divs bg-white p-2 border border-light">
    <form
      @submit.prevent="authenticateUser" 
      id="login_form"
      class="d-flex flex-column align-items-center p-2 rounded"
      method="POST"
    >
      <div class="mb-3 w-100">
        <input
          type="email"
          name="email"
          class="form-label border w-100 p-2 border-light rounded"
          id="login_email"
          placeholder="Enter email"
          required
        />
      </div>
      <div id="password_box" class="mb-3 w-100">
        <i id="eye-icon" @click="pass_visibility" class="fa-solid fa-eye-slash"></i>
        <input
          type="password"
          name="password"
          class="form-label border w-100 p-2 border-light rounded"
          id="login_password"
          placeholder="Enter password"
        />
      </div>
      <div>
        <button
          
          type="submit"
          class="btn btn-primary w-100"
        >
          Login
        </button>
        
      </div>
      <hr />
    </form>
    <div class="d-flex flex-column align-items-center">
      <p>New user? Please sign up first</p>
      <button
        id="sign-up-button"
        type="button"
        class="btn btn-success"
        @click="signUpView"
      >
        Sign up
      </button>
    </div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'

export default {
  name: "HomeView",
  components: {
  },
  data() {
    return {
      userAuthenticated : false,
    }
  },
  methods:{
    pass_visibility: function(){
      let pass = document.getElementById("login_password");
      let eyeIcon = document.getElementById("eye-icon");
      if(pass.type == "password"){
        pass.type = 'text'
        eyeIcon.classList.replace('fa-eye-slash', 'fa-eye')
      }
      else{
        pass.type = 'password'
        eyeIcon.classList.replace('fa-eye', 'fa-eye-slash')
      }
    },
    testwebhook: async function(){
      let msg = {
        'text': 'Hello from a VUE JS!'}
      const response = await fetch('https://chat.googleapis.com/v1/spaces/AAAALDg1w4U/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=gV9dwwrY0KJfH2aIqgPLb5M6EeW5WbNvcLeDhmX37ZA%3D',{
        method: "POST",
        body: JSON.stringify(msg)
      })
      .then((response) => response.json())
      .then((data) => console.log(data))
    },
    testfunc: async function(){
      const response = await fetch('http://localhost:8000/testapi')
      .then((response) => response.json())
      .then((data) => console.log(data))
    },
    authenticateUser: async function(){
      let login_form = document.getElementById("login_form");
      let form_data =  new FormData(login_form);
      const response = await fetch('http://localhost:8000/api/login', {
        method: 'POST',
        body: form_data,
        credentials: 'include',
      }).then((response) => {
        console.log(response.status)
        if(response.status == 400){
          throw new Error("Something went wrong!");
        }
        return response.json()
        })
      .then((data) => {
        console.log(data)
        // let access_token = data.access_token;
        // console.log(access_token);
        if(data.login){
          // localStorage.setItem('access_token', access_token);
          this.$router.push('/dashboard')
          Vue.notify({
            group: 'foo',
            type: 'success',
            title: 'Successfully logged in!',
            text: ''
          });
        }
        else{
          Vue.notify({
                group: 'foo',
                type: 'warn',
                title: 'Invalid email/password!',
                text: 'Please retype the correct info.'
              });
        }
    })
    .catch((err) => {
      console.error("ERROR",err)
      this.$router.replace('/error')
      })
    },
    signUpView: function(){
      this.$router.push('/signup')
    }
  }
};
</script>

<style scoped>
  .vue-notification{
    margin-top: 10px;
  }
  #login_form{
    width: 300px;
  }
  #eye-icon{
    position: absolute;
    margin-top:13px;
    margin-left: 240px;
  }
</style>