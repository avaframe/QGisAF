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
    <rasterrenderer classificationMax="100" nodataColor="" band="1" classificationMin="0" alphaBand="-1" type="singlebandpseudocolor" opacity="1">
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
        <colorrampshader clip="0" maximumValue="100" labelPrecision="6" classificationMode="1" minimumValue="0" colorRampType="DISCRETE">
          <colorramp name="[source]" type="gradient">
            <Option type="Map">
              <Option name="color1" type="QString" value="255,245,235,0"/>
              <Option name="color2" type="QString" value="32,17,88,255"/>
              <Option name="discrete" type="QString" value="0"/>
              <Option name="rampType" type="QString" value="gradient"/>
              <Option name="stops" type="QString" value="0.01;255,245,235,0:0.05;255,206,244,255:0.1;255,167,168,255:0.15;193,154,27,255:0.2;87,139,33,255:0.25;0,112,84,255:0.3;0,73,96,255"/>
            </Option>
            <prop k="color1" v="255,245,235,0"/>
            <prop k="color2" v="32,17,88,255"/>
            <prop k="discrete" v="0"/>
            <prop k="rampType" v="gradient"/>
            <prop k="stops" v="0.01;255,245,235,0:0.05;255,206,244,255:0.1;255,167,168,255:0.15;193,154,27,255:0.2;87,139,33,255:0.25;0,112,84,255:0.3;0,73,96,255"/>
          </colorramp>
          <item color="#fff5eb" label="&lt;= 1 m/s" alpha="0" value="1"/>
          <item color="#ffcef4" label="1 - 5 m/s" alpha="255" value="5"/>
          <item color="#ffa7a8" label="5 - 10 m/s" alpha="255" value="10"/>
          <item color="#c19a1b" label="10 - 15 m/s" alpha="255" value="15"/>
          <item color="#578b21" label="15 - 20 m/s" alpha="255" value="20"/>
          <item color="#007054" label="20 - 25 m/s" alpha="255" value="25"/>
          <item color="#004960" label="25 - 30 m/s" alpha="255" value="30"/>
          <item color="#201158" label="> 30 m/s" alpha="255" value="100"/>
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
