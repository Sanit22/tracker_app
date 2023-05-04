import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";
import DashBoardView from "../views/DashBoardView.vue"
import Error from "../views/Error.vue"
import LogFormView from "../views/LogFormView.vue"
import ViewLogs from "../views/ViewLogs.vue"
import TrackerForm from "../views/TrackerForm.vue"
import SignUpView from "../views/SignUpView.vue"

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/dashboard", 
    name: "dashboard",
    component: DashBoardView,
  },
  {
    path: "/error",
    name: "error",
    component: Error
  }, 
  {
    path: "/log_form/:tracker_id/:action/:log_id?",
    name: "log_form",
    component: LogFormView
  },
  {
    path: "/view_logs/:tracker_id",
    name: "view_logs",
    component: ViewLogs
  },
  {
    path: "/tracker_form/:action/:tracker_id?",
    name: "tracker_form",
    component: TrackerForm
  },
  {
    path: "/signup",
    name: "signup_form",
    component: SignUpView
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
