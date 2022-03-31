import { Component, Vue, Inject } from 'vue-property-decorator';

import { ICountry } from '@/shared/model/country.model';
import CountryService from './country.service';
import AlertService from '@/shared/alert/alert.service';

@Component
export default class CountryDetails extends Vue {
  @Inject('countryService') private countryService: () => CountryService;
  @Inject('alertService') private alertService: () => AlertService;

  public country: ICountry = {};

  beforeRouteEnter(to, from, next) {
    next(vm => {
      if (to.params.countryId) {
        vm.retrieveCountry(to.params.countryId);
      }
    });
  }

  public retrieveCountry(countryId) {
    this.countryService()
      .find(countryId)
      .then(res => {
        this.country = res;
      })
      .catch(error => {
        this.alertService().showHttpError(this, error.response);
      });
  }

  public previousState() {
    this.$router.go(-1);
  }
}
