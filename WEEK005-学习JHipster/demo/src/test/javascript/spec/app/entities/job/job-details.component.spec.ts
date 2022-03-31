/* tslint:disable max-line-length */
import { shallowMount, createLocalVue, Wrapper } from '@vue/test-utils';
import sinon, { SinonStubbedInstance } from 'sinon';
import VueRouter from 'vue-router';

import * as config from '@/shared/config/config';
import JobDetailComponent from '@/entities/job/job-details.vue';
import JobClass from '@/entities/job/job-details.component';
import JobService from '@/entities/job/job.service';
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
  describe('Job Management Detail Component', () => {
    let wrapper: Wrapper<JobClass>;
    let comp: JobClass;
    let jobServiceStub: SinonStubbedInstance<JobService>;

    beforeEach(() => {
      jobServiceStub = sinon.createStubInstance<JobService>(JobService);

      wrapper = shallowMount<JobClass>(JobDetailComponent, {
        store,
        i18n,
        localVue,
        router,
        provide: { jobService: () => jobServiceStub, alertService: () => new AlertService() },
      });
      comp = wrapper.vm;
    });

    describe('OnInit', () => {
      it('Should call load all on init', async () => {
        // GIVEN
        const foundJob = { id: 123 };
        jobServiceStub.find.resolves(foundJob);

        // WHEN
        comp.retrieveJob(123);
        await comp.$nextTick();

        // THEN
        expect(comp.job).toBe(foundJob);
      });
    });

    describe('Before route enter', () => {
      it('Should retrieve data', async () => {
        // GIVEN
        const foundJob = { id: 123 };
        jobServiceStub.find.resolves(foundJob);

        // WHEN
        comp.beforeRouteEnter({ params: { jobId: 123 } }, null, cb => cb(comp));
        await comp.$nextTick();

        // THEN
        expect(comp.job).toBe(foundJob);
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
