import { Component, Vue, Inject } from 'vue-property-decorator';

import { ITask } from '@/shared/model/task.model';
import TaskService from './task.service';
import AlertService from '@/shared/alert/alert.service';

@Component
export default class TaskDetails extends Vue {
  @Inject('taskService') private taskService: () => TaskService;
  @Inject('alertService') private alertService: () => AlertService;

  public task: ITask = {};

  beforeRouteEnter(to, from, next) {
    next(vm => {
      if (to.params.taskId) {
        vm.retrieveTask(to.params.taskId);
      }
    });
  }

  public retrieveTask(taskId) {
    this.taskService()
      .find(taskId)
      .then(res => {
        this.task = res;
      })
      .catch(error => {
        this.alertService().showHttpError(this, error.response);
      });
  }

  public previousState() {
    this.$router.go(-1);
  }
}
