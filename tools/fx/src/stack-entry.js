/* Entry for /assets/stack.js, loaded by the hand-written skill pages (which do not load
   site.js). The generated pages get the same code through motion.js. */
import { auto } from './stack.js';

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', auto);
else auto();
