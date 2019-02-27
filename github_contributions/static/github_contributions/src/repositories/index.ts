import {PolymerElement, html} from '@polymer/polymer';
import {mixinBehaviors} from '@polymer/polymer/lib/legacy/class.js';
import {NeonAnimatableBehavior} from '@polymer/neon-animation/neon-animatable-behavior.js';

class SampleElement extends mixinBehaviors([NeonAnimatableBehavior], PolymerElement) {
  static get template() {
    return html`
      <style>
        :host {
          display: block;
          
          
        }
      </style>

      <slot></slot>
    `;
  }
}
customElements.define('sample-element', SampleElement);
