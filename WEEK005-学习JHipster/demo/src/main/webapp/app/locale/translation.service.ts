import axios from 'axios';
import VueI18n from 'vue-i18n';
import { Store } from 'vuex';
import dayjs from 'dayjs';

export default class TranslationService {
  private store: Store<unknown>;
  private i18n: VueI18n;

  constructor(store: Store<unknown>, i18n: VueI18n) {
    this.store = store;
    this.i18n = i18n;
  }

  public refreshTranslation(newLanguage: string) {
    let currentLanguage = this.store.getters.currentLanguage;
    currentLanguage = newLanguage ? newLanguage : 'zh-cn';
    if (this.i18n && !this.i18n.messages[currentLanguage]) {
      this.i18n.setLocaleMessage(currentLanguage, {});
      axios.get(`i18n/${currentLanguage}.json?_=${I18N_HASH}`).then((res: any) => {
        if (res.data) {
          this.i18n.setLocaleMessage(currentLanguage, res.data);
          this.setLocale(currentLanguage);
        }
      });
    } else if (this.i18n) {
      this.setLocale(currentLanguage);
    }
  }

  private setLocale(lang: string) {
    dayjs.locale(lang);
    this.i18n.locale = lang;
    this.store.commit('currentLanguage', lang);
    axios.defaults.headers.common['Accept-Language'] = lang;
    document.querySelector('html').setAttribute('lang', lang);
  }
}
