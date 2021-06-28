<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" minScale="1e+08" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" version="3.18.3-Zürich">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal fetchMode="0" mode="0" enabled="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <property key="WMSBackgroundLayer" value="false"/>
    <property key="WMSPublishDataSourceUrl" value="false"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="identify/format" value="Value"/>
  </customproperties>
  <pipe>
    <provider>
      <resampling enabled="false" maxOversampling="2" zoomedInResamplingMethod="nearestNeighbour" zoomedOutResamplingMethod="nearestNeighbour"/>
    </provider>
    <rasterrenderer classificationMax="1000" nodataColor="" band="1" classificationMin="1" alphaBand="-1" type="singlebandpseudocolor" opacity="0.698">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Exact</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader clip="0" maximumValue="1000" labelPrecision="6" classificationMode="1" minimumValue="1" colorRampType="DISCRETE">
          <colorramp name="[source]" type="gradient">
            <Option type="Map">
              <Option name="color1" type="QString" value="247,251,255,0"/>
              <Option name="color2" type="QString" value="139,0,105,255"/>
              <Option name="discrete" type="QString" value="0"/>
              <Option name="rampType" type="QString" value="gradient"/>
              <Option name="stops" type="QString" value="0.00900901;176,244,250,255:0.024024;117,193,101,255:0.049049;169,108,0,255"/>
            </Option>
            <prop k="color1" v="247,251,255,0"/>
            <prop k="color2" v="139,0,105,255"/>
            <prop k="discrete" v="0"/>
            <prop k="rampType" v="gradient"/>
            <prop k="stops" v="0.00900901;176,244,250,255:0.024024;117,193,101,255:0.049049;169,108,0,255"/>
          </colorramp>
          <item color="#f7fbff" label="&lt;= 1 kPa" alpha="0" value="1"/>
          <item color="#b0f4fa" label="1 - 10 kPa" alpha="255" value="10"/>
          <item color="#75c165" label="10 - 25 kPa" alpha="255" value="25"/>
          <item color="#a96c00" label="25 - 50 kPa" alpha="255" value="50"/>
          <item color="#8b0069" label="> 50 kPa" alpha="255" value="1000"/>
          <rampLegendSettings maximumLabel="" prefix="" orientation="2" minimumLabel="" useContinuousLegend="1" suffix="" direction="0">
            <numericFormat id="basic">
              <Option type="Map">
                <Option name="decimal_separator" type="QChar" value=""/>
                <Option name="decimals" type="int" value="6"/>
                <Option name="rounding_type" type="int" value="0"/>
                <Option name="show_plus" type="bool" value="false"/>
                <Option name="show_thousand_separator" type="bool" value="true"/>
                <Option name="show_trailing_zeros" type="bool" value="false"/>
                <Option name="thousand_separator" type="QChar" value=""/>
              </Option>
            </numericFormat>
          </rampLegendSettings>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast contrast="0" brightness="0" gamma="1"/>
    <huesaturation colorizeBlue="128" colorizeGreen="128" grayscaleMode="0" colorizeStrength="100" saturation="0" colorizeOn="0" colorizeRed="255"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
