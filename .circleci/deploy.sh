#!/usr/bin/env bash
set -e;

# Determine the configuration name
if [ "$CIRCLE_BRANCH" == "production" ]; then
	export ZAPPA_ENVIRONMENT="production";
else
	export ZAPPA_ENVIRONMENT="dev";
fi;

echo "------------------------------------------------";
echo -e "\n\nDeploying Lambda function with Zappa\n\n"
echo "------------------------------------------------";
echo -e "Zappa environment detected: ${ZAPPA_ENVIRONMENT}\n\n";

echo "----------------------";
echo "zappa_settings.json:";
echo "----------------------";
cat zappa_settings.json;
echo -e "\n\n";

# Download the configuration
echo "Downloading cloud configuration";
aws s3 cp $DEPLOYMENT_CONFIG_FILE config.json;

# Load current Zappa Settings
echo "Loading current settings from zappa file...";
ZAPPA_SETTINGS=$(cat zappa_settings.json);

for CONFIG_KEY in $(jq -c --raw-output ".${ZAPPA_ENVIRONMENT} | keys[]" config.json); do
    # Get the key's value
    CONFIG_KEY_VALUE=$(jq -c --raw-output ".${ZAPPA_ENVIRONMENT}.${CONFIG_KEY}" config.json);
    
    if [[ $CONFIG_KEY_VALUE != *"{"* ]]; then
        CONFIG_KEY_VALUE="\"$CONFIG_KEY_VALUE\"";
    fi
    echo $CONFIG_KEY_VALUE;

    # Assign the current key and it's value to our current zappa settings, and save (patch) ...
    echo "Generating new zappa settings...";
    ZAPPA_SETTINGS=$(echo $ZAPPA_SETTINGS | jq -r ".${ZAPPA_ENVIRONMENT}.${CONFIG_KEY} = ${CONFIG_KEY_VALUE}");
done;

echo "Saving changes..."
echo $ZAPPA_SETTINGS > zappa_settings.json;


echo "----------------------";
echo "zappa_settings.json:";
echo "----------------------";
cat zappa_settings.json;
echo -e "\n\n";


echo -e "\n\n";

# Deploy (assume the function is already there)
echo "Running Zappa : $(date)";
pipenv run zappa update $ZAPPA_ENVIRONMENT;
