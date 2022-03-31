/* tslint:disable max-line-length */
import { shallowMount, createLocalVue, Wrapper } from '@vue/test-utils';
import sinon, { SinonStubbedInstance } from 'sinon';
import Router from 'vue-router';
import { ToastPlugin } from 'bootstrap-vue';

import dayjs from 'dayjs';
import { DATE_TIME_LONG_FORMAT } from '@/shared/date/filters';

import * as config from '@/shared/config/config';
import JobHistoryUpdateComponent from '@/entities/job-history/job-history-update.vue';
import JobHistoryClass from '@/entities/job-history/job-history-update.component';
import JobHistoryService from '@/entities/job-history/job-history.service';

import JobService from '@/entities/job/job.service';

import DepartmentService from '@/entities/department/department.service';

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
  describe('JobHistory Management Update Component', () => {
    let wrapper: Wrapper<JobHistoryClass>;
    let comp: JobHistoryClass;
    let jobHistoryServiceStub: SinonStubbedInstance<JobHistoryService>;

    beforeEach(() => {
      jobHistoryServiceStub = sinon.createStubInstance<JobHistoryService>(JobHistoryService);

      wrapper = shallowMount<JobHistoryClass>(JobHistoryUpdateComponent, {
        store,
        i18n,
        localVue,
        router,
        provide: {
          jobHistoryService: () => jobHistoryServiceStub,
          alertService: () => new AlertService(),

          jobService: () =>
            sinon.createStubInstance<JobService>(JobService, {
              retrieve: sinon.stub().resolves({}),
            } as any),

          departmentService: () =>
            sinon.createStubInstance<DepartmentService>(DepartmentService, {
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

    describe('load', () => {
      it('Should convert date from string', () => {
        // GIVEN
        const date = new Date('2019-10-15T11:42:02Z');

        // WHEN
        const convertedDate = comp.convertDateTimeFromServer(date);

        // THEN
        expect(convertedDate).toEqual(dayjs(date).format(DATE_TIME_LONG_FORMAT));
      });

      it('Should not convert date if date is not present', () => {
        expect(comp.convertDateTimeFromServer(null)).toBeNull();
      });
    });

    describe('save', () => {
      it('Should call update service on save for existing entity', async () => {
        // GIVEN
        const entity = { id: 123 };
        comp.jobHistory = entity;
        jobHistoryServiceStub.update.resolves(entity);

        // WHEN
        comp.save();
        await comp.$nextTick();

        // THEN
        expect(jobHistoryServiceStub.update.calledWith(entity)).toBeTruthy();
        expect(comp.isSaving).toEqual(false);
      });

      it('Should call create service on save for new entity', async () => {
        // GIVEN
        const entity = {};
        comp.jobHistory = entity;
        jobHistoryServiceStub.create.resolves(entity);

        // WHEN
        comp.save();
        await comp.$nextTick();

        // THEN
        expect(jobHistoryServiceStub.create.calledWith(entity)).toBeTruthy();
        expect(comp.isSaving).toEqual(false);
      });
    });

    describe('Before route enter', () => {
      it('Should retrieve data', async () => {
        // GIVEN
        const foundJobHistory = { id: 123 };
        jobHistoryServiceStub.find.resolves(foundJobHistory);
        jobHistoryServiceStub.retrieve.resolves([foundJobHistory]);

        // WHEN
        comp.beforeRouteEnter({ params: { jobHistoryId: 123 } }, null, cb => cb(comp));
        await comp.$nextTick();

        // THEN
        expect(comp.jobHistory).toBe(foundJobHistory);
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
