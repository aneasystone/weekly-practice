import { Component, Vue, Inject } from 'vue-property-decorator';

import { ILocation } from '@/shared/model/location.model';
import LocationService from './location.service';
import AlertService from '@/shared/alert/alert.service';

@Component
export default class LocationDetails extends Vue {
  @Inject('locationService') private locationService: () => LocationService;
  @Inject('alertService') private alertService: () => AlertService;

  public location: ILocation = {};

  beforeRouteEnter(to, from, next) {
    next(vm => {
      if (to.params.locationId) {
        vm.retrieveLocation(to.params.locationId);
      }
    });
  }

  public retrieveLocation(locationId) {
    this.locationService()
      .find(locationId)
      .then(res => {
        this.location = res;
      })
      .catch(error => {
        this.alertService().showHttpError(this, error.response);
      });
  }

  public previousState() {
    this.$router.go(-1);
  }
}
