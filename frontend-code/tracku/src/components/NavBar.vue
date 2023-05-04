<template>
    
    <nav id="navbar" class="navbar navbar-expand-lg navbar-light text-white w-100">
        <div class="container-fluid">
            <p class="navbar-brand mt-2">
                <router-link class="text-decoration-none text-white ms-4 fs-3" to="/dashboard"> TrackU </router-link>
            </p>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse offset-md-3 text-white" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0 ">
                    <li class="nav-item">
                        <router-link to="/dashboard" class="nav-link active text-white" aria-current="page">Dashboard</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link :to="{ name: 'tracker_form', params: { action: 'create'} }" class="nav-link active text-white"> Create tracker </router-link>
                    </li>
                    <li class="nav-item">
                        <a @click="logOutUser" class="nav-link active text-white" aria-current="page">Log out</a>
                    </li>     
                </ul>
            </div> 
        </div>
    </nav>

</template>

<script>

export default {
    name: 'NavBar',
    methods:{
        logOutUser: async function(){
            const response = await fetch('http://localhost:8000/api/logout',{
                credentials:'include'
            }) 
            .then((response) => response.json())
            .then((data) => {
                console.log(data)
                 this.$router.replace({ path: '/' })
            })
        }

    }
}

</script>


<style scoped>
#navbar{
    background-color: rgb(63, 63, 63);
    color: white;
}

.nav-link:hover{
    text-decoration: underline;
}
</style>