package com.lieutenantdan.intonare;

import android.os.Bundle;
import android.webkit.PermissionRequest;
import com.getcapacitor.BridgeActivity;
import com.getcapacitor.BridgeWebChromeClient;

public class MainActivity extends BridgeActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Extend Capacitor's own WebChromeClient rather than replacing it
        getBridge().getWebView().setWebChromeClient(
            new BridgeWebChromeClient(getBridge()) {
                @Override
                public void onPermissionRequest(PermissionRequest request) {
                    runOnUiThread(() -> request.grant(request.getResources()));
                }
            }
        );
    }
}
