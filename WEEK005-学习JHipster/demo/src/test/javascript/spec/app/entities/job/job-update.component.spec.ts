/* tslint:disable max-line-length */
import { shallowMount, createLocalVue, Wrapper } from '@vue/test-utils';
import sinon, { SinonStubbedInstance } from 'sinon';
import Router from 'vue-router';
import { ToastPlugin } from 'bootstrap-vue';

import * as config from '@/shared/config/config';
import JobUpdateComponent from '@/entities/job/job-update.vue';
import JobClass from '@/entities/job/job-update.component';
import JobService from '@/entities/job/job.service';

import TaskService from '@/entities/task/task.service';

import EmployeeService from '@/entities/employee/employee.service';
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
  describe('Job Management Update Component', () => {
    let wrapper: Wrapper<JobClass>;
    let comp: JobClass;
    let jobServiceStub: SinonStubbedInstance<JobService>;

    beforeEach(() => {
      jobServiceStub = sinon.createStubInstance<JobService>(JobService);

      wrapper = shallowMount<JobClass>(JobUpdateComponent, {
        store,
        i18n,
        localVue,
        router,
        provide: {
          jobService: () => jobServiceStub,
          alertService: () => new AlertService(),

          taskService: () =>
            sinon.createStubInstance<TaskService>(TaskService, {
              retrieve: sinon.stub().resolves({}),
            } as any),

          employeeService: () =>
            sinon.createStubInstance<EmployeeService>(EmployeeService, {
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
        comp.job = entity;
        jobServiceStub.update.resolves(entity);

        // WHEN
        comp.save();
        await comp.$nextTick();

        // THEN
        expect(jobServiceStub.update.calledWith(entity)).toBeTruthy();
        expect(comp.isSaving).toEqual(false);
      });

      it('Should call create service on save for new entity', async () => {
        // GIVEN
        const entity = {};
        comp.job = entity;
        jobServiceStub.create.resolves(entity);

        // WHEN
        comp.save();
        await comp.$nextTick();

        // THEN
        expect(jobServiceStub.create.calledWith(entity)).toBeTruthy();
        expect(comp.isSaving).toEqual(false);
      });
    });

    describe('Before route enter', () => {
      it('Should retrieve data', async () => {
        // GIVEN
        const foundJob = { id: 123 };
        jobServiceStub.find.resolves(foundJob);
        jobServiceStub.retrieve.resolves([foundJob]);

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
