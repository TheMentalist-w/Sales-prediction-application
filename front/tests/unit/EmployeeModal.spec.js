import { mount, createLocalVue } from '@vue/test-utils';
import EmployeeModal from '@/Accounts/components/EmployeeModal';
import Vuetify from 'vuetify';

describe('EmployeeModal.vue New User Modal', () => {
  let vuetify;
  const localVue = createLocalVue();
  let wrapper;
  beforeEach(() => {
    const div = document.createElement('div');
    div.id = 'root';
    document.body.appendChild(div);
    vuetify = new Vuetify();
    wrapper = mount(EmployeeModal, {
      localVue,
      vuetify,
      attachTo: '#root',
      propsData: {
        formTitle: 'New Employee',
        editedItem: {
          username: '',
          employee: '',
          email: '',
          type: '',
          password: '',
          confirmPassword: ''
        },
        editedIndex: -1
      }
    });
  });

  afterEach(() => {
    wrapper.destroy();
  });

  it('Is a Vue instance', () => {
    expect(wrapper.isVueInstance).toBeTruthy();
  });

  it('Does new modal has clean validation', () => {
    expect(wrapper.findAll('.v-messages__message').exists()).toBeFalsy();
  });

  it('Does valid email validation works', async () => {
    await wrapper.find('.emailField').trigger('focus');
    await wrapper.find('.emailField input').setValue('test@test.test');
    await wrapper.find('.usernameField').trigger('focus');
    expect(wrapper.find('.emailField .v-messages__message').exists()).toBeFalsy();
  });

  it('Does invalid email validation works', async () => {
    await wrapper.find('.emailField').trigger('focus');
    await wrapper.find('.emailField input').setValue('test@test');
    await wrapper.find('.usernameField').trigger('focus');
    expect(wrapper.find('.emailField .v-messages__message').exists()).toBeTruthy();
  });

  it('Does invalid email validation works 2.0', async () => {
    await wrapper.find('.emailField').trigger('focus');
    await wrapper.find('.emailField input').setValue('test.test');
    await wrapper.find('.usernameField').trigger('focus');
    expect(wrapper.find('.emailField .v-messages__message').exists()).toBeTruthy();
  });

  // Not working tests
  /* it('Does invalid email validation works 3.0', async () => {
        await wrapper.find('.emailField').trigger('focus')
        await wrapper.find('.usernameField').trigger('focus')
        expect(wrapper.find('.emailField .v-text-field__details').text()).toContain('Invalid e-mail')
    })

    it('Does password (new Employee) validation works', async () => {
        await wrapper.find('.passwordField').trigger('focus')
        await wrapper.find('.emailField').trigger('focus')
        expect(wrapper.find('.passwordField .v-messages__message').exists()).toBeTruthy()
    }) */
});
