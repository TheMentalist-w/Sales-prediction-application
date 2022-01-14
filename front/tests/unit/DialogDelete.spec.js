import { mount, createLocalVue } from '@vue/test-utils';
import DialogDelete from '@/Accounts/components/DialogDelete';
import Vuetify from 'vuetify';
import VueRouter from 'vue-router';

describe('DialogDelete.vue', () => {
  let vuetify;
  const localVue = createLocalVue();
  localVue.use(VueRouter);
  let wrapper;
  let router;
  beforeEach(() => {
    const div = document.createElement('div');
    div.id = 'root';
    document.body.appendChild(div);
    vuetify = new Vuetify();
    router = new VueRouter();
    wrapper = mount(DialogDelete, {
      localVue,
      vuetify,
      router,
      attachTo: '#root'
    });
  });

  afterEach(() => {
    wrapper.destroy();
  });
  it('Is a Vue instance', () => {
    expect(wrapper.isVueInstance).toBeTruthy();
  });
});
