/* tslint:disable max-line-length */
import { shallowMount, createLocalVue, Wrapper } from '@vue/test-utils';
import sinon, { SinonStubbedInstance } from 'sinon';
import Router from 'vue-router';
import { ToastPlugin } from 'bootstrap-vue';

import * as config from '@/shared/config/config';
import LocationUpdateComponent from '@/entities/location/location-update.vue';
import LocationClass from '@/entities/location/location-update.component';
import LocationService from '@/entities/location/location.service';

import CountryService from '@/entities/country/country.service';
import AlertService from '@/shared/alert/alert.service';

const localVue = createLocalVue();

config.initVueApp(localVue);
const i18n = config.initI18N(localVue);
const store = config.initVueXStore(localVue);
const router = new Router();
localVue.use(Router);
localVue.use(ToastPlugin);
localVue.component('font-awesome-icon', {});
localVue.component('b-input-group', {});
localVue.component('b-input-group-prepend', {});
localVue.component('b-form-datepicker', {});
localVue.component('b-form-input', {});

describe('Component Tests', () => {
  describe('Location Management Update Component', () => {
    let wrapper: Wrapper<LocationClass>;
    let comp: LocationClass;
    let locationServiceStub: SinonStubbedInstance<LocationService>;

    beforeEach(() => {
      locationServiceStub = sinon.createStubInstance<LocationService>(LocationService);

      wrapper = shallowMount<LocationClass>(LocationUpdateComponent, {
        store,
        i18n,
        localVue,
        router,
        provide: {
          locationService: () => locationServiceStub,
          alertService: () => new AlertService(),

          countryService: () =>
            sinon.createStubInstance<CountryService>(CountryService, {
              retrieve: sinon.stub().resolves({}),
            } as any),
        },
      });
      comp = wrapper.vm;
    });

    describe('save', () => {
      it('Should call update service on save for existing entity', async () => {
        // GIVEN
        const entity = { id: 123 };
        comp.location = entity;
        locationServiceStub.update.resolves(entity);

        // WHEN
        comp.save();
        await comp.$nextTick();

        // THEN
        expect(locationServiceStub.update.calledWith(entity)).toBeTruthy();
        expect(comp.isSaving).toEqual(false);
      });

      it('Should call create service on save for new entity', async () => {
        // GIVEN
        const entity = {};
        comp.location = entity;
        locationServiceStub.create.resolves(entity);

        // WHEN
        comp.save();
        await comp.$nextTick();

        // THEN
        expect(locationServiceStub.create.calledWith(entity)).toBeTruthy();
        expect(comp.isSaving).toEqual(false);
      });
    });

    describe('Before route enter', () => {
      it('Should retrieve data', async () => {
        // GIVEN
        const foundLocation = { id: 123 };
        locationServiceStub.find.resolves(foundLocation);
        locationServiceStub.retrieve.resolves([foundLocation]);

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
