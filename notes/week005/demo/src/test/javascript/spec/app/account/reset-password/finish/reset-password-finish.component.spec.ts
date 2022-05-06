import axios from 'axios';
import sinon from 'sinon';
import * as config from '@/shared/config/config';
import { createLocalVue, shallowMount, Wrapper } from '@vue/test-utils';
import ResetPasswordFinish from '@/account/reset-password/finish/reset-password-finish.vue';
import ResetPasswordFinishClass from '@/account/reset-password/finish/reset-password-finish.component';
import LoginService from '@/account/login.service';

const localVue = createLocalVue();

config.initVueApp(localVue);
const i18n = config.initI18N(localVue);

const axiosStub = {
  get: sinon.stub(axios, 'get'),
  post: sinon.stub(axios, 'post'),
};

describe('Reset Component Finish', () => {
  let wrapper: Wrapper<ResetPasswordFinishClass>;
  let resetPasswordFinish: ResetPasswordFinishClass;

  beforeEach(() => {
    axiosStub.post.reset();
    wrapper = shallowMount<ResetPasswordFinishClass>(ResetPasswordFinish, {
      i18n,
      localVue,
      provide: {
        loginService: () => new LoginService(),
      },
    });
    resetPasswordFinish = wrapper.vm;
  });

  it('should reset finish be a success', async () => {
    // Given
    axiosStub.post.resolves();

    // When
    await resetPasswordFinish.finishReset();

    // Then
    expect(resetPasswordFinish.success).toBeTruthy();
  });

  it('should reset request fail as an error', async () => {
    // Given
    axiosStub.post.rejects({
      response: {
        status: null,
        data: {
          type: null,
        },
      },
    });

    // When
    resetPasswordFinish.finishReset();
    await resetPasswordFinish.$nextTick();

    // Then
    expect(resetPasswordFinish.success).toBeNull();
    expect(resetPasswordFinish.error).toEqual('ERROR');
  });
});
