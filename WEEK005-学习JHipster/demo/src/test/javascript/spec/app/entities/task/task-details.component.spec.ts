/* tslint:disable max-line-length */
import { shallowMount, createLocalVue, Wrapper } from '@vue/test-utils';
import sinon, { SinonStubbedInstance } from 'sinon';
import VueRouter from 'vue-router';

import * as config from '@/shared/config/config';
import TaskDetailComponent from '@/entities/task/task-details.vue';
import TaskClass from '@/entities/task/task-details.component';
import TaskService from '@/entities/task/task.service';
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
  describe('Task Management Detail Component', () => {
    let wrapper: Wrapper<TaskClass>;
    let comp: TaskClass;
    let taskServiceStub: SinonStubbedInstance<TaskService>;

    beforeEach(() => {
      taskServiceStub = sinon.createStubInstance<TaskService>(TaskService);

      wrapper = shallowMount<TaskClass>(TaskDetailComponent, {
        store,
        i18n,
        localVue,
        router,
        provide: { taskService: () => taskServiceStub, alertService: () => new AlertService() },
      });
      comp = wrapper.vm;
    });

    describe('OnInit', () => {
      it('Should call load all on init', async () => {
        // GIVEN
        const foundTask = { id: 123 };
        taskServiceStub.find.resolves(foundTask);

        // WHEN
        comp.retrieveTask(123);
        await comp.$nextTick();

        // THEN
        expect(comp.task).toBe(foundTask);
      });
    });

    describe('Before route enter', () => {
      it('Should retrieve data', async () => {
        // GIVEN
        const foundTask = { id: 123 };
        taskServiceStub.find.resolves(foundTask);

        // WHEN
        comp.beforeRouteEnter({ params: { taskId: 123 } }, null, cb => cb(comp));
        await comp.$nextTick();

        // THEN
        expect(comp.task).toBe(foundTask);
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
