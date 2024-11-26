package io.ionic.starter;

import android.os.Bundle;
import com.getcapacitor.BridgeActivity;
import android.webkit.WebView;
import android.webkit.WebSettings;

public class MainActivity extends BridgeActivity {
  @Override
  public void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);

    // Obtén la instancia de WebView utilizada por Capacitor
    WebView webView = this.bridge.getWebView();
    WebSettings webSettings = webView.getSettings();

    // Configura el modo de contenido mixto para permitir contenido no seguro
    if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.LOLLIPOP) {
      webSettings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
    }
  }
}
