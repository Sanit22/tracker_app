<template>
<div id="signup_form" class="mx-auto">
   <h1 class="pt-3 mt-3 text-decoration-underline"> Sign up form </h1> 
    <form
       @submit.prevent="submitForm" 
      id="signup_form"
      class="d-flex flex-column align-items-center p-2 w-100 rounded mt-3"
      method="POST"
    >
      <div class="mb-3 w-100">
        <input
          name="name"
          type="text"
          class="form-label border w-100 p-2 border-light rounded"
          id="username"
          placeholder="Enter your name"
          required
        />
      </div>

      <div class="mb-3 w-100">
        <input
          name="email"
          type="email"
          class="form-label border w-100 p-2 border-light rounded"
          id="email"
          placeholder="Enter email"
          required
        />
      </div>

      <div class="mb-3 w-100">
        <i id="eye-icon-pass" @click="pass_visibility" class="fa-solid fa-eye-slash eye-icon"></i>
        <input
          name="password"
          v-model="password"
          type="password"
          class="form-label border w-100 p-2 border-light rounded"
          id="password"
          placeholder="Enter password"
        />
        <p class="fs-6 fw-lighter fst-italic"> (Between 8 - 15 chars with 1 uppercase, 1 lowercase, 1 digit & 1 special char)</p>
        <p v-if="!checkPasswordValid && password.length > 0"> Password must fulfill the criteria </p>
      </div>

      <div class="mb-3 w-100">
        <i id="eye-icon-conpass" @click="con_pass_visibility" class="fa-solid fa-eye-slash eye-icon"></i>
        <input
          v-model="confirmPassword" 
          type="password"
          class="form-label border w-100 p-2 border-light rounded"
          id="confirm_password"
          placeholder="Confirm password"
        />
        <p v-if="!confirmPasswordValid && confirmPassword.length > 0">   Must be the same as password </p>
      </div>
      <div>
        <button type="submit" class="btn btn-primary w-100">Sign up</button>
      </div>
      <!-- <p class="mt-3" v-if="!submit_success"> All fields must satisfy the criteria! </p> -->
      <hr />
    </form>
    <div class="d-flex flex-column align-items-center">
      <p >Already registered ? Please login</p>
      <button
        @click="loginPage"
        id="login-button" 
        type="button"
        class="btn btn-success"
      >
        Login
      </button>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
    export default{
        name: 'SignUpView',
        data(){
            return{
                regex: /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,15}$/,
                password:'',
                confirmPassword: '',
                submit_success: true,
            }
        },
        computed:{
            checkPasswordValid: function(){
                
                console.log("INSIDE CHECKPASS")
                // const pass_element = document.getElementById("password")
                if(this.password.match(this.regex)){
                    // pass_element.style.borderColor = 'black'
                    return true
                }
                else{
                    // pass_element.style.borderColor = 'red'
                    return false
                }
            },
            confirmPasswordValid: function(){
                if(this.confirmPassword !== this.password){
                    return false
                }
                else{
                    return true
                }
            }
        },
        methods:{
            pass_visibility: function(){
                let pass = document.getElementById("password");
                let eyeIcon = document.getElementById("eye-icon-pass");
                if(pass.type == "password"){
                  pass.type = 'text'
                  eyeIcon.classList.replace('fa-eye-slash', 'fa-eye')
                }
                else{
                  pass.type = 'password'
                  eyeIcon.classList.replace('fa-eye', 'fa-eye-slash')
                }
            },
            con_pass_visibility: function(){
                let pass = document.getElementById("confirm_password");
                let eyeIcon = document.getElementById("eye-icon-conpass");
                if(pass.type == "password"){
                  pass.type = 'text'
                  eyeIcon.classList.replace('fa-eye-slash', 'fa-eye')
                }
                else{
                  pass.type = 'password'
                  eyeIcon.classList.replace('fa-eye', 'fa-eye-slash')
                }
            },
            submitForm: async function(){
                if(this.checkPasswordValid && this.confirmPasswordValid){
                    this.submit_success = true
                    let form_elem = document.getElementById("signup_form")
                    let form_data = new FormData(form_elem)
                    console.log(form_data)
                    const response = await fetch('http://localhost:8000/api/signup',{
                        method:'POST',
                        credentials:'include',
                        body: form_data
                    })
                    .then((response) => {
                      if(response.status === 400){
                        Vue.notify({
                          group: 'foo',
                          type: 'warn',
                          title: 'Something went wrong!',
                          text: 'Please submit again.'
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
                          title: 'Successfully signed up!',
                          text: 'Please login to continue.'
                        });
                        this.$router.push('/')
                    })
                }
                else{
                   Vue.notify({
                    group: 'foo',
                    type: 'warn',
                    title: 'Incorect info entered!',
                    text: 'Please retype the correct info.'
                  });
                    this.submit_success = false
                }
            },
            loginPage: function(){
                this.$router.push('/')
            }
        }
    }
</script>

<style scoped>
.eye-icon{
    position: absolute;
    margin-top:13px;
    margin-left: 240px;
}

#signup_form{
  width:300px;
}
</style>