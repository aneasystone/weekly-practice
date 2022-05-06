import { Component, Vue, Inject } from 'vue-property-decorator';
import Vue2Filters from 'vue2-filters';
import { ITask } from '@/shared/model/task.model';

import TaskService from './task.service';
import AlertService from '@/shared/alert/alert.service';

@Component({
  mixins: [Vue2Filters.mixin],
})
export default class Task extends Vue {
  @Inject('taskService') private taskService: () => TaskService;
  @Inject('alertService') private alertService: () => AlertService;

  private removeId: number = null;

  public tasks: ITask[] = [];

  public isFetching = false;

  public mounted(): void {
    this.retrieveAllTasks();
  }

  public clear(): void {
    this.retrieveAllTasks();
  }

  public retrieveAllTasks(): void {
    this.isFetching = true;
    this.taskService()
      .retrieve()
      .then(
        res => {
          this.tasks = res.data;
          this.isFetching = false;
        },
        err => {
          this.isFetching = false;
          this.alertService().showHttpError(this, err.response);
        }
      );
  }

  public handleSyncList(): void {
    this.clear();
  }

  public prepareRemove(instance: ITask): void {
    this.removeId = instance.id;
    if (<any>this.$refs.removeEntity) {
      (<any>this.$refs.removeEntity).show();
    }
  }

  public removeTask(): void {
    this.taskService()
      .delete(this.removeId)
      .then(() => {
        const message = this.$t('demoApp.task.deleted', { param: this.removeId });
        this.$bvToast.toast(message.toString(), {
          toaster: 'b-toaster-top-center',
          title: 'Info',
          variant: 'danger',
          solid: true,
          autoHideDelay: 5000,
        });
        this.removeId = null;
        this.retrieveAllTasks();
        this.closeDialog();
      })
      .catch(error => {
        this.alertService().showHttpError(this, error.response);
      });
  }

  public closeDialog(): void {
    (<any>this.$refs.removeEntity).hide();
  }
}
