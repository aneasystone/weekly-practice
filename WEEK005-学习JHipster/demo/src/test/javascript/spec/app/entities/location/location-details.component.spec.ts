/* tslint:disable max-line-length */
import { shallowMount, createLocalVue, Wrapper } from '@vue/test-utils';
import sinon, { SinonStubbedInstance } from 'sinon';
import VueRouter from 'vue-router';

import * as config from '@/shared/config/config';
import LocationDetailComponent from '@/entities/location/location-details.vue';
import LocationClass from '@/entities/location/location-details.component';
import LocationService from '@/entities/location/location.service';
import router from '@/router';
import AlertService from '@/shared/alert/alert.service';

const localVue = createLocalVue();
localVue.use(VueRouter);

config.initVueApp(localVue);
const i18n = config.initI18N(localVue);
const store = config.initVueXStore(localVue);
localVue.component('font-awesome-icon', {});
localVue.component('router-link', {});

describe('Component Tests', () => {
  describe('Location Management Detail Component', () => {
    let wrapper: Wrapper<LocationClass>;
    let comp: LocationClass;
    let locationServiceStub: SinonStubbedInstance<LocationService>;

    beforeEach(() => {
      locationServiceStub = sinon.createStubInstance<LocationService>(LocationService);

      wrapper = shallowMount<LocationClass>(LocationDetailComponent, {
        store,
        i18n,
        localVue,
        router,
        provide: { locationService: () => locationServiceStub, alertService: () => new AlertService() },
      });
      comp = wrapper.vm;
    });

    describe('OnInit', () => {
      it('Should call load all on init', async () => {
        // GIVEN
        const foundLocation = { id: 123 };
        locationServiceStub.find.resolves(foundLocation);

        // WHEN
        comp.retrieveLocation(123);
        await comp.$nextTick();

        // THEN
        expect(comp.location).toBe(foundLocation);
      });
    });

    describe('Before route enter', () => {
      it('Should retrieve data', async () => {
        // GIVEN
        const foundLocation = { id: 123 };
        locationServiceStub.find.resolves(foundLocation);

        // WHEN
        comp.beforeRouteEnter({ params: { locationId: 123 } }, null, cb => cb(comp));
        await comp.$nextTick();

        // THEN
        expect(comp.location).toBe(foundLocation);
      });
    });

    describe('Previous state', () => {
      it('Should go previous state', async () => {
        comp.previousState();
        await comp.$nextTick();

        expect(comp.$router.currentRoute.fullPath).toContain('/');
      });
    });
  });
});
