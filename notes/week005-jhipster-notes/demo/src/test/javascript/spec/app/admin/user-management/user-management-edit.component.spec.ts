import { shallowMount, createLocalVue, Wrapper } from '@vue/test-utils';
import axios from 'axios';
import sinon from 'sinon';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

import * as config from '@/shared/config/config';
import UserManagementEdit from '@/admin/user-management/user-management-edit.vue';
import UserManagementEditClass from '@/admin/user-management/user-management-edit.component';
import UserManagementService from '@/admin/user-management/user-management.service';
import VueRouter from 'vue-router';
import { ToastPlugin } from 'bootstrap-vue';
import AlertService from '@/shared/alert/alert.service';

const localVue = createLocalVue();
localVue.use(VueRouter);
localVue.use(ToastPlugin);

config.initVueApp(localVue);
const i18n = config.initI18N(localVue);
const store = config.initVueXStore(localVue);
localVue.component('font-awesome-icon', FontAwesomeIcon);

const axiosStub = {
  get: sinon.stub(axios, 'get'),
  post: sinon.stub(axios, 'post'),
  put: sinon.stub(axios, 'put'),
};

describe('UserManagementEdit Component', () => {
  let wrapper: Wrapper<UserManagementEditClass>;
  let userManagementEdit: UserManagementEditClass;

  beforeEach(() => {
    const router = new VueRouter();
    wrapper = shallowMount<UserManagementEditClass>(UserManagementEdit, {
      store,
      router,
      i18n,
      localVue,
      provide: {
        userManagementService: () => new UserManagementService(),
        alertService: () => new AlertService(),
      },
    });
    userManagementEdit = wrapper.vm;
  });

  describe('init', () => {
    it('Should load user', async () => {
      // GIVEN
      axiosStub.get.resolves({});

      // WHEN
      userManagementEdit.init(123);
      await userManagementEdit.$nextTick();

      // THEN
      expect(axiosStub.get.calledWith('api/admin/users/' + 123)).toBeTruthy();
    });
  });

  describe('initAuthorities', () => {
    it('Should load authorities', async () => {
      // GIVEN
      axiosStub.get.resolves({});

      // WHEN
      userManagementEdit.initAuthorities();
      await userManagementEdit.$nextTick();

      // THEN
      expect(axiosStub.get.calledWith(`api/authorities`)).toBeTruthy();
    });
  });

  describe('save', () => {
    it('Should call update service on save for existing user', async () => {
      // GIVEN
      axiosStub.put.resolves({
        headers: {
          'x-demoapp-alert': '',
          'x-demoapp-params': '',
        },
      });
      userManagementEdit.userAccount = { id: 123, authorities: [] };

      // WHEN
      userManagementEdit.save();
      await userManagementEdit.$nextTick();

      // THEN
      expect(axiosStub.put.calledWith('api/admin/users', { id: 123, authorities: [] })).toBeTruthy();
      expect(userManagementEdit.isSaving).toEqual(false);
    });

    it('Should call create service on save for new user', async () => {
      // GIVEN
      axiosStub.post.resolves({
        headers: {
          'x-demoapp-alert': '',
          'x-demoapp-params': '',
        },
      });
      userManagementEdit.userAccount = { authorities: [] };

      // WHEN
      userManagementEdit.save();
      await userManagementEdit.$nextTick();

      // THEN
      expect(axiosStub.post.calledWith('api/admin/users', { authorities: [] })).toBeTruthy();
      expect(userManagementEdit.isSaving).toEqual(false);
    });
  });
});
