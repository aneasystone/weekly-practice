import { createLocalVue, Wrapper, shallowMount } from '@vue/test-utils';
import Error from '@/core/error/error.vue';
import ErrorClass from '@/core/error/error.component';
import * as config from '@/shared/config/config';
import router from '@/router';
import LoginService from '@/account/login.service';

const localVue = createLocalVue();
config.initVueApp(localVue);
const i18n = config.initI18N(localVue);
const store = config.initVueXStore(localVue);
const customErrorMsg = 'An error occurred.';

describe('Error component', () => {
  let error: ErrorClass;
  let wrapper: Wrapper<ErrorClass>;
  let loginService: LoginService;

  beforeEach(() => {
    loginService = { openLogin: jest.fn() };
    wrapper = shallowMount<ErrorClass>(Error, {
      i18n,
      store,
      router,
      localVue,
      provide: {
        loginService: () => loginService,
      },
    });
    error = wrapper.vm;
  });

  it('should have retrieve custom error on routing', () => {
    error.beforeRouteEnter({ meta: { errorMessage: customErrorMsg } }, null, cb => cb(error));

    expect(error.errorMessage).toBe(customErrorMsg);
    expect(error.error403).toBeFalsy();
    expect(error.error404).toBeFalsy();
    expect(loginService.openLogin).toHaveBeenCalledTimes(0);
  });

  it('should have set forbidden error on routing', () => {
    error.beforeRouteEnter({ meta: { error403: true } }, null, cb => cb(error));

    expect(error.errorMessage).toBeNull();
    expect(error.error403).toBeTruthy();
    expect(error.error404).toBeFalsy();
    expect(loginService.openLogin).toHaveBeenCalled();
  });

  it('should have set not found error on routing', () => {
    error.beforeRouteEnter({ meta: { error404: true } }, null, cb => cb(error));

    expect(error.errorMessage).toBeNull();
    expect(error.error403).toBeFalsy();
    expect(error.error404).toBeTruthy();
    expect(loginService.openLogin).toHaveBeenCalledTimes(0);
  });

  it('should have retrieve custom error on init', () => {
    error.init(customErrorMsg, false, false);

    expect(error.errorMessage).toBe(customErrorMsg);
    expect(error.error403).toBeFalsy();
    expect(error.error404).toBeFalsy();
    expect(loginService.openLogin).toHaveBeenCalledTimes(0);
  });

  it('should have set forbidden error on init', () => {
    error.init(null, true, false);

    expect(error.errorMessage).toBeNull();
    expect(error.error403).toBeTruthy();
    expect(error.error404).toBeFalsy();
    expect(loginService.openLogin).toHaveBeenCalled();
  });

  it('should have set not found error on init', () => {
    error.init(null, false, true);

    expect(error.errorMessage).toBeNull();
    expect(error.error403).toBeFalsy();
    expect(error.error404).toBeTruthy();
    expect(loginService.openLogin).toHaveBeenCalledTimes(0);
  });

  it('should have set default on init', () => {
    error.init();

    expect(error.errorMessage).toBeNull();
    expect(error.error403).toBeFalsy();
    expect(error.error404).toBeFalsy();
    expect(loginService.openLogin).toHaveBeenCalledTimes(0);
  });
});
