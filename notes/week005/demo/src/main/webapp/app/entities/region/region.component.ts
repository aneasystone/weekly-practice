import { Component, Vue, Inject } from 'vue-property-decorator';
import Vue2Filters from 'vue2-filters';
import { IRegion } from '@/shared/model/region.model';

import RegionService from './region.service';
import AlertService from '@/shared/alert/alert.service';

@Component({
  mixins: [Vue2Filters.mixin],
})
export default class Region extends Vue {
  @Inject('regionService') private regionService: () => RegionService;
  @Inject('alertService') private alertService: () => AlertService;

  private removeId: number = null;

  public regions: IRegion[] = [];

  public isFetching = false;

  public mounted(): void {
    this.retrieveAllRegions();
  }

  public clear(): void {
    this.retrieveAllRegions();
  }

  public retrieveAllRegions(): void {
    this.isFetching = true;
    this.regionService()
      .retrieve()
      .then(
        res => {
          this.regions = res.data;
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

  public prepareRemove(instance: IRegion): void {
    this.removeId = instance.id;
    if (<any>this.$refs.removeEntity) {
      (<any>this.$refs.removeEntity).show();
    }
  }

  public removeRegion(): void {
    this.regionService()
      .delete(this.removeId)
      .then(() => {
        const message = this.$t('demoApp.region.deleted', { param: this.removeId });
        this.$bvToast.toast(message.toString(), {
          toaster: 'b-toaster-top-center',
          title: 'Info',
          variant: 'danger',
          solid: true,
          autoHideDelay: 5000,
        });
        this.removeId = null;
        this.retrieveAllRegions();
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
