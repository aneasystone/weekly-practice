import { Component, Vue, Inject } from 'vue-property-decorator';
import Vue2Filters from 'vue2-filters';
import { ILocation } from '@/shared/model/location.model';

import LocationService from './location.service';
import AlertService from '@/shared/alert/alert.service';

@Component({
  mixins: [Vue2Filters.mixin],
})
export default class Location extends Vue {
  @Inject('locationService') private locationService: () => LocationService;
  @Inject('alertService') private alertService: () => AlertService;

  private removeId: number = null;

  public locations: ILocation[] = [];

  public isFetching = false;

  public mounted(): void {
    this.retrieveAllLocations();
  }

  public clear(): void {
    this.retrieveAllLocations();
  }

  public retrieveAllLocations(): void {
    this.isFetching = true;
    this.locationService()
      .retrieve()
      .then(
        res => {
          this.locations = res.data;
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

  public prepareRemove(instance: ILocation): void {
    this.removeId = instance.id;
    if (<any>this.$refs.removeEntity) {
      (<any>this.$refs.removeEntity).show();
    }
  }

  public removeLocation(): void {
    this.locationService()
      .delete(this.removeId)
      .then(() => {
        const message = this.$t('demoApp.location.deleted', { param: this.removeId });
        this.$bvToast.toast(message.toString(), {
          toaster: 'b-toaster-top-center',
          title: 'Info',
          variant: 'danger',
          solid: true,
          autoHideDelay: 5000,
        });
        this.removeId = null;
        this.retrieveAllLocations();
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
