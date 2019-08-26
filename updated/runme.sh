#!/bin/bash  

echo "###Update client"
cp -rf Search/directives/index.ts /opt/superdesk/client/node_modules/superdesk-core/scripts/apps/search/directives/
echo "index.ts  ...Copied"
sleep 1 
cp -rf Search/directives/RepoDropdown.ts /opt/superdesk/client/node_modules/superdesk-core/scripts/apps/search/directives/
echo "RepoDropdown.ts  ...Copied"
sleep 1 
cp -rf Search/directives/SearchParametersTop.ts /opt/superdesk/client/node_modules/superdesk-core/scripts/apps/search/directives/
echo "SearchParametersTop.ts  ...Copied"
sleep 1 
cp -rf Search/views/repo-dropdown.html /opt/superdesk/client/node_modules/superdesk-core/scripts/apps/search/views/
echo "repo-dropdown.html  ...Copied"
sleep 1 
cp -rf Search/views/search.html /opt/superdesk/client/node_modules/superdesk-core/scripts/apps/search/views/
echo "search.html  ...Copied"
sleep 1 
cp -rf Search/views/search-parametersTop.html /opt/superdesk/client/node_modules/superdesk-core/scripts/apps/search/views/
echo "search-parametersTop.html  ...Copied"
sleep 1 
cp -rf Search/index.ts /opt/superdesk/client/node_modules/superdesk-core/scripts/apps/search/
echo "index.ts  ...Copied"
sleep 1 
cp -rf arabization/ar.po /opt/superdesk/client/node_modules/superdesk-core/po/
echo "ar.po  ...Copied"
sleep 1 
cp -rf edit-form.html /opt/superdesk/client/node_modules/superdesk-core/scripts/apps/users/views/
echo "edit-form.html  ...Copied"
sleep 1 
cp -rf ingest-sources-content.html /opt/superdesk/client/node_modules/superdesk-core/scripts/apps/ingest/views/settings/
echo "ingest-sources-content.html  ...Copied"
sleep 1 
cp -rf ItemRendition.ts /opt/superdesk/client/node_modules/superdesk-core/scripts/apps/archive/directives/
echo "ItemRendition.ts  ...Copied"
sleep 1 
cp -rf login-modal.html /opt/superdesk/client/node_modules/superdesk-core/scripts/core/auth/
echo "login-modal.html  ...Copied"
sleep 1 
cp -rf menu.html /opt/superdesk/client/node_modules/superdesk-core/scripts/core/menu/views/
echo "menu.html  ...Copied"
sleep 1 
cp -rf pageTitle.ts /opt/superdesk/client/node_modules/superdesk-core/scripts/core/services/
echo "pageTitle.ts  ...Copied"
sleep 1 
cp -rf phone-home-modal-directive.html /opt/superdesk/client/node_modules/superdesk-core/scripts/core/directives/views/
echo "phone-home-modal-directive.html  ...Copied"
sleep 1 
cp -rf preview.html /opt/superdesk/client/node_modules/superdesk-core/scripts/apps/archive/views/
echo "preview.html  ...Copied"
sleep 1 
cp -rf products-config-modal.html /opt/superdesk/client/node_modules/superdesk-core/scripts/apps/products/views/
echo "products-config-modal.html  ...Copied"
sleep 1 
cp -rf reset-password.html /opt/superdesk/client/node_modules/superdesk-core/scripts/core/auth/
echo "reset-password.html  ...Copied"
sleep 1 
cp -rf secure-login.html /opt/superdesk/client/node_modules/superdesk-core/scripts/core/auth/
echo "secure-login.html  ...Copied"
sleep 1 
cp -rf settings-roles.html /opt/superdesk/client/node_modules/superdesk-core/scripts/apps/users/views/
echo "settings-roles.html  ...Copied"
sleep 1 
cp -rf superdesk-view.html /opt/superdesk/client/node_modules/superdesk-core/scripts/core/menu/views/
echo "superdesk-view.html  ...Copied"
sleep 1 
cp -rf WekalatLogo.png /opt/superdesk/client/node_modules/superdesk-core/images/
echo "WekalatLogo.png  ...Copied"
sleep 1 
cp -rf workspace-sidenav.html /opt/superdesk/client/node_modules/superdesk-core/scripts/apps/workspace/views/
echo "workspace-sidenav.html  ...Copied"

echo "###Update server"
cp -rf server/dpa_newsml_2_0.py /opt/superdesk/env/src/superdesk-core/superdesk/io/feed_parsers/
echo "dpa_newsml_2_0.py  ...Copied"
sleep 1 
cp -rf server/newsml_1_2_new.py /opt/superdesk/env/src/superdesk-core/superdesk/io/feed_parsers/
echo "newsml_1_2_new.py  ...Copied"
sleep 1 
cp -rf server/__init__.py /opt/superdesk/env/src/superdesk-core/superdesk/io/feed_parsers/
echo "__init__.py  ...Copied"
sleep 1 

cp -rf ClientConfig/superdesk.config.js /opt/superdesk/client/
echo "ClientConfig.config.js root  ...Copied"
sleep 1 
cp -rf ClientConfig/inner/superdesk.config.js /opt/superdesk/client/node_modules/superdesk-core/
echo "ClientConfig.config.js inner  ...Copied"
sleep 1 

echo "###restart superdesk server"
cd /opt/superdesk/client/
grunt build

echo "###restart superdesk server"
sudo systemctl restart superdesk

