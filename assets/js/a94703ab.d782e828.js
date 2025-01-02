"use strict";(self.webpackChunkmonolith_docs=self.webpackChunkmonolith_docs||[]).push([[48],{411:(e,t,a)=>{a.r(t),a.d(t,{default:()=>ge});var n=a(6540),o=a(4164),i=a(1003),s=a(7559),l=a(4718),r=a(609),c=a(1312),d=a(3104),u=a(5062);const m={backToTopButton:"backToTopButton_sjWU",backToTopButtonShow:"backToTopButtonShow_xfvO"};var h=a(4848);function b(){const{shown:e,scrollToTop:t}=function(e){let{threshold:t}=e;const[a,o]=(0,n.useState)(!1),i=(0,n.useRef)(!1),{startScroll:s,cancelScroll:l}=(0,d.gk)();return(0,d.Mq)(((e,a)=>{let{scrollY:n}=e;const s=a?.scrollY;s&&(i.current?i.current=!1:n>=s?(l(),o(!1)):n<t?o(!1):n+window.innerHeight<document.documentElement.scrollHeight&&o(!0))})),(0,u.$)((e=>{e.location.hash&&(i.current=!0,o(!1))})),{shown:a,scrollToTop:()=>s(0)}}({threshold:300});return(0,h.jsx)("button",{"aria-label":(0,c.T)({id:"theme.BackToTopButton.buttonAriaLabel",message:"Scroll back to top",description:"The ARIA label for the back to top button"}),className:(0,o.A)("clean-btn",s.G.common.backToTopButton,m.backToTopButton,e&&m.backToTopButtonShow),type:"button",onClick:t})}var p=a(3109),x=a(6347),j=a(4581),f=a(6342),g=a(8774),v=a(6025),A=a(4586),_=a(1122);function C(e){let{logo:t,alt:a,imageClassName:n}=e;const o={light:(0,v.Ay)(t.src),dark:(0,v.Ay)(t.srcDark||t.src)},i=(0,h.jsx)(_.A,{className:t.className,sources:o,height:t.height,width:t.width,alt:a,style:t.style});return n?(0,h.jsx)("div",{className:n,children:i}):i}function k(e){const{siteConfig:{title:t}}=(0,A.A)(),{navbar:{title:a,logo:n}}=(0,f.p)(),{imageClassName:o,titleClassName:i,...s}=e,l=(0,v.Ay)(n?.href||"/"),r=a?"":t,c=n?.alt??r;return(0,h.jsxs)(g.A,{to:l,...s,...n?.target&&{target:n.target},children:[n&&(0,h.jsx)(C,{logo:n,alt:c,imageClassName:o}),null!=a&&(0,h.jsx)("b",{className:i,children:a})]})}function N(e){return(0,h.jsx)("svg",{width:"20",height:"20","aria-hidden":"true",...e,children:(0,h.jsxs)("g",{fill:"#7a7a7a",children:[(0,h.jsx)("path",{d:"M9.992 10.023c0 .2-.062.399-.172.547l-4.996 7.492a.982.982 0 01-.828.454H1c-.55 0-1-.453-1-1 0-.2.059-.403.168-.551l4.629-6.942L.168 3.078A.939.939 0 010 2.528c0-.548.45-.997 1-.997h2.996c.352 0 .649.18.828.45L9.82 9.472c.11.148.172.347.172.55zm0 0"}),(0,h.jsx)("path",{d:"M19.98 10.023c0 .2-.058.399-.168.547l-4.996 7.492a.987.987 0 01-.828.454h-3c-.547 0-.996-.453-.996-1 0-.2.059-.403.168-.551l4.625-6.942-4.625-6.945a.939.939 0 01-.168-.55 1 1 0 01.996-.997h3c.348 0 .649.18.828.45l4.996 7.492c.11.148.168.347.168.55zm0 0"})]})})}const S="collapseSidebarButton_PEFL",T="collapseSidebarButtonIcon_kv0_";function I(e){let{onClick:t}=e;return(0,h.jsx)("button",{type:"button",title:(0,c.T)({id:"theme.docs.sidebar.collapseButtonTitle",message:"Collapse sidebar",description:"The title attribute for collapse button of doc sidebar"}),"aria-label":(0,c.T)({id:"theme.docs.sidebar.collapseButtonAriaLabel",message:"Collapse sidebar",description:"The title attribute for collapse button of doc sidebar"}),className:(0,o.A)("button button--secondary button--outline",S),onClick:t,children:(0,h.jsx)(N,{className:T})})}var y=a(5041),B=a(9532);const w=Symbol("EmptyContext"),L=n.createContext(w);function E(e){let{children:t}=e;const[a,o]=(0,n.useState)(null),i=(0,n.useMemo)((()=>({expandedItem:a,setExpandedItem:o})),[a]);return(0,h.jsx)(L.Provider,{value:i,children:t})}var M=a(1422),H=a(9169),G=a(2303);function P(e){let{collapsed:t,categoryLabel:a,onClick:n}=e;return(0,h.jsx)("button",{"aria-label":t?(0,c.T)({id:"theme.DocSidebarItem.expandCategoryAriaLabel",message:"Expand sidebar category '{label}'",description:"The ARIA label to expand the sidebar category"},{label:a}):(0,c.T)({id:"theme.DocSidebarItem.collapseCategoryAriaLabel",message:"Collapse sidebar category '{label}'",description:"The ARIA label to collapse the sidebar category"},{label:a}),"aria-expanded":!t,type:"button",className:"clean-btn menu__caret",onClick:n})}function R(e){let{item:t,onItemClick:a,activePath:i,level:r,index:c,...d}=e;const{items:u,label:m,collapsible:b,className:p,href:x}=t,{docs:{sidebar:{autoCollapseCategories:j}}}=(0,f.p)(),v=function(e){const t=(0,G.A)();return(0,n.useMemo)((()=>e.href&&!e.linkUnlisted?e.href:!t&&e.collapsible?(0,l.Nr)(e):void 0),[e,t])}(t),A=(0,l.w8)(t,i),_=(0,H.ys)(x,i),{collapsed:C,setCollapsed:k}=(0,M.u)({initialState:()=>!!b&&(!A&&t.collapsed)}),{expandedItem:N,setExpandedItem:S}=function(){const e=(0,n.useContext)(L);if(e===w)throw new B.dV("DocSidebarItemsExpandedStateProvider");return e}(),T=function(e){void 0===e&&(e=!C),S(e?null:c),k(e)};return function(e){let{isActive:t,collapsed:a,updateCollapsed:o}=e;const i=(0,B.ZC)(t);(0,n.useEffect)((()=>{t&&!i&&a&&o(!1)}),[t,i,a,o])}({isActive:A,collapsed:C,updateCollapsed:T}),(0,n.useEffect)((()=>{b&&null!=N&&N!==c&&j&&k(!0)}),[b,N,c,k,j]),(0,h.jsxs)("li",{className:(0,o.A)(s.G.docs.docSidebarItemCategory,s.G.docs.docSidebarItemCategoryLevel(r),"menu__list-item",{"menu__list-item--collapsed":C},p),children:[(0,h.jsxs)("div",{className:(0,o.A)("menu__list-item-collapsible",{"menu__list-item-collapsible--active":_}),children:[(0,h.jsx)(g.A,{className:(0,o.A)("menu__link",{"menu__link--sublist":b,"menu__link--sublist-caret":!x&&b,"menu__link--active":A}),onClick:b?e=>{a?.(t),x?T(!1):(e.preventDefault(),T())}:()=>{a?.(t)},"aria-current":_?"page":void 0,role:b&&!x?"button":void 0,"aria-expanded":b&&!x?!C:void 0,href:b?v??"#":v,...d,children:m}),x&&b&&(0,h.jsx)(P,{collapsed:C,categoryLabel:m,onClick:e=>{e.preventDefault(),T()}})]}),(0,h.jsx)(M.N,{lazy:!0,as:"ul",className:"menu__list",collapsed:C,children:(0,h.jsx)(q,{items:u,tabIndex:C?-1:0,onItemClick:a,activePath:i,level:r+1})})]})}var W=a(6654),D=a(3186);const F="menuExternalLink_NmtK";function U(e){let{item:t,onItemClick:a,activePath:n,level:i,index:r,...c}=e;const{href:d,label:u,className:m,autoAddBaseUrl:b}=t,p=(0,l.w8)(t,n),x=(0,W.A)(d);return(0,h.jsx)("li",{className:(0,o.A)(s.G.docs.docSidebarItemLink,s.G.docs.docSidebarItemLinkLevel(i),"menu__list-item",m),children:(0,h.jsxs)(g.A,{className:(0,o.A)("menu__link",!x&&F,{"menu__link--active":p}),autoAddBaseUrl:b,"aria-current":p?"page":void 0,to:d,...x&&{onClick:a?()=>a(t):void 0},...c,children:[u,!x&&(0,h.jsx)(D.A,{})]})},u)}const V="menuHtmlItem_M9Kj";function Y(e){let{item:t,level:a,index:n}=e;const{value:i,defaultStyle:l,className:r}=t;return(0,h.jsx)("li",{className:(0,o.A)(s.G.docs.docSidebarItemLink,s.G.docs.docSidebarItemLinkLevel(a),l&&[V,"menu__list-item"],r),dangerouslySetInnerHTML:{__html:i}},n)}function K(e){let{item:t,...a}=e;switch(t.type){case"category":return(0,h.jsx)(R,{item:t,...a});case"html":return(0,h.jsx)(Y,{item:t,...a});default:return(0,h.jsx)(U,{item:t,...a})}}function z(e){let{items:t,...a}=e;const n=(0,l.Y)(t,a.activePath);return(0,h.jsx)(E,{children:n.map(((e,t)=>(0,h.jsx)(K,{item:e,index:t,...a},t)))})}const q=(0,n.memo)(z),O="menu_SIkG",J="menuWithAnnouncementBar_GW3s";function Q(e){let{path:t,sidebar:a,className:i}=e;const l=function(){const{isActive:e}=(0,y.M)(),[t,a]=(0,n.useState)(e);return(0,d.Mq)((t=>{let{scrollY:n}=t;e&&a(0===n)}),[e]),e&&t}();return(0,h.jsx)("nav",{"aria-label":(0,c.T)({id:"theme.docs.sidebar.navAriaLabel",message:"Docs sidebar",description:"The ARIA label for the sidebar navigation"}),className:(0,o.A)("menu thin-scrollbar",O,l&&J,i),children:(0,h.jsx)("ul",{className:(0,o.A)(s.G.docs.docSidebarMenu,"menu__list"),children:(0,h.jsx)(q,{items:a,activePath:t,level:1})})})}const X="sidebar_njMd",Z="sidebarWithHideableNavbar_wUlq",$="sidebarHidden_VK0M",ee="sidebarLogo_isFc";function te(e){let{path:t,sidebar:a,onCollapse:n,isHidden:i}=e;const{navbar:{hideOnScroll:s},docs:{sidebar:{hideable:l}}}=(0,f.p)();return(0,h.jsxs)("div",{className:(0,o.A)(X,s&&Z,i&&$),children:[s&&(0,h.jsx)(k,{tabIndex:-1,className:ee}),(0,h.jsx)(Q,{path:t,sidebar:a}),l&&(0,h.jsx)(I,{onClick:n})]})}const ae=n.memo(te);var ne=a(5600),oe=a(9876);const ie=e=>{let{sidebar:t,path:a}=e;const n=(0,oe.M)();return(0,h.jsx)("ul",{className:(0,o.A)(s.G.docs.docSidebarMenu,"menu__list"),children:(0,h.jsx)(q,{items:t,activePath:a,onItemClick:e=>{"category"===e.type&&e.href&&n.toggle(),"link"===e.type&&n.toggle()},level:1})})};function se(e){return(0,h.jsx)(ne.GX,{component:ie,props:e})}const le=n.memo(se);function re(e){const t=(0,j.l)(),a="desktop"===t||"ssr"===t,n="mobile"===t;return(0,h.jsxs)(h.Fragment,{children:[a&&(0,h.jsx)(ae,{...e}),n&&(0,h.jsx)(le,{...e})]})}const ce={expandButton:"expandButton_TmdG",expandButtonIcon:"expandButtonIcon_i1dp"};function de(e){let{toggleSidebar:t}=e;return(0,h.jsx)("div",{className:ce.expandButton,title:(0,c.T)({id:"theme.docs.sidebar.expandButtonTitle",message:"Expand sidebar",description:"The ARIA label and title attribute for expand button of doc sidebar"}),"aria-label":(0,c.T)({id:"theme.docs.sidebar.expandButtonAriaLabel",message:"Expand sidebar",description:"The ARIA label and title attribute for expand button of doc sidebar"}),tabIndex:0,role:"button",onKeyDown:t,onClick:t,children:(0,h.jsx)(N,{className:ce.expandButtonIcon})})}const ue={docSidebarContainer:"docSidebarContainer_YfHR",docSidebarContainerHidden:"docSidebarContainerHidden_DPk8",sidebarViewport:"sidebarViewport_aRkj"};function me(e){let{children:t}=e;const a=(0,r.t)();return(0,h.jsx)(n.Fragment,{children:t},a?.name??"noSidebar")}function he(e){let{sidebar:t,hiddenSidebarContainer:a,setHiddenSidebarContainer:i}=e;const{pathname:l}=(0,x.zy)(),[r,c]=(0,n.useState)(!1),d=(0,n.useCallback)((()=>{r&&c(!1),!r&&(0,p.O)()&&c(!0),i((e=>!e))}),[i,r]);return(0,h.jsx)("aside",{className:(0,o.A)(s.G.docs.docSidebarContainer,ue.docSidebarContainer,a&&ue.docSidebarContainerHidden),onTransitionEnd:e=>{e.currentTarget.classList.contains(ue.docSidebarContainer)&&a&&c(!0)},children:(0,h.jsx)(me,{children:(0,h.jsxs)("div",{className:(0,o.A)(ue.sidebarViewport,r&&ue.sidebarViewportHidden),children:[(0,h.jsx)(re,{sidebar:t,path:l,onCollapse:d,isHidden:r}),r&&(0,h.jsx)(de,{toggleSidebar:d})]})})})}const be={docMainContainer:"docMainContainer_TBSr",docMainContainerEnhanced:"docMainContainerEnhanced_lQrH",docItemWrapperEnhanced:"docItemWrapperEnhanced_JWYK"};function pe(e){let{hiddenSidebarContainer:t,children:a}=e;const n=(0,r.t)();return(0,h.jsx)("main",{className:(0,o.A)(be.docMainContainer,(t||!n)&&be.docMainContainerEnhanced),children:(0,h.jsx)("div",{className:(0,o.A)("container padding-top--md padding-bottom--lg",be.docItemWrapper,t&&be.docItemWrapperEnhanced),children:a})})}const xe={docRoot:"docRoot_UBD9",docsWrapper:"docsWrapper_hBAB"};function je(e){let{children:t}=e;const a=(0,r.t)(),[o,i]=(0,n.useState)(!1);return(0,h.jsxs)("div",{className:xe.docsWrapper,children:[(0,h.jsx)(b,{}),(0,h.jsxs)("div",{className:xe.docRoot,children:[a&&(0,h.jsx)(he,{sidebar:a.items,hiddenSidebarContainer:o,setHiddenSidebarContainer:i}),(0,h.jsx)(pe,{hiddenSidebarContainer:o,children:t})]})]})}var fe=a(3363);function ge(e){const t=(0,l.B5)(e);if(!t)return(0,h.jsx)(fe.A,{});const{docElement:a,sidebarName:n,sidebarItems:c}=t;return(0,h.jsx)(i.e3,{className:(0,o.A)(s.G.page.docsDocPage),children:(0,h.jsx)(r.V,{name:n,items:c,children:(0,h.jsx)(je,{children:a})})})}},3363:(e,t,a)=>{a.d(t,{A:()=>l});a(6540);var n=a(4164),o=a(1312),i=a(1107),s=a(4848);function l(e){let{className:t}=e;return(0,s.jsx)("main",{className:(0,n.A)("container margin-vert--xl",t),children:(0,s.jsx)("div",{className:"row",children:(0,s.jsxs)("div",{className:"col col--6 col--offset-3",children:[(0,s.jsx)(i.A,{as:"h1",className:"hero__title",children:(0,s.jsx)(o.A,{id:"theme.NotFound.title",description:"The title of the 404 page",children:"Page Not Found"})}),(0,s.jsx)("p",{children:(0,s.jsx)(o.A,{id:"theme.NotFound.p1",description:"The first paragraph of the 404 page",children:"We could not find what you were looking for."})}),(0,s.jsx)("p",{children:(0,s.jsx)(o.A,{id:"theme.NotFound.p2",description:"The 2nd paragraph of the 404 page",children:"Please contact the owner of the site that linked you to the original URL and let them know their link is broken."})})]})})})}}}]);