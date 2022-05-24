<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="1000" minScale="1e+08" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" version="3.18.3-Zürich">
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
    <rasterrenderer classificationMax="0.66131252263468" nodataColor="" band="1" classificationMin="0" alphaBand="-1" type="singlebandpseudocolor" opacity="1">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>CumulativeCut</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader clip="0" maximumValue="0.6613125226346804" labelPrecision="6" classificationMode="1" minimumValue="0" colorRampType="DISCRETE">
          <colorramp name="[source]" type="gradient">
            <Option type="Map">
              <Option name="color1" type="QString" value="254,230,206,0"/>
              <Option name="color2" type="QString" value="4,4,4,255"/>
              <Option name="discrete" type="QString" value="0"/>
              <Option name="rampType" type="QString" value="gradient"/>
              <Option name="stops" type="QString" value="0.198462;254,230,206,0:0.396925;255,254,158,255:0.793849;244,171,67,255:1.19077;212,96,100,255:1.5877;145,49,110,255:1.98462;68,29,78,255"/>
            </Option>
            <prop k="color1" v="254,230,206,0"/>
            <prop k="color2" v="4,4,4,255"/>
            <prop k="discrete" v="0"/>
            <prop k="rampType" v="gradient"/>
            <prop k="stops" v="0.198462;254,230,206,0:0.396925;255,254,158,255:0.793849;244,171,67,255:1.19077;212,96,100,255:1.5877;145,49,110,255:1.98462;68,29,78,255"/>
          </colorramp>
          <item color="#fee6ce" label=" &lt;= 0.5 m" alpha="0" value="0.5"/>
          <item color="#fffe9e" label="0.5 - 1 m" alpha="255" value="1"/>
          <item color="#f4ab43" label="1 - 2 m" alpha="255" value="2"/>
          <item color="#d46064" label="2 -3 m" alpha="255" value="3"/>
          <item color="#91316e" label="3 - 4 m" alpha="255" value="4"/>
          <item color="#441d4e" label="4 - 5 m" alpha="255" value="5"/>
          <item color="#040404" label=" > 5 m" alpha="255" value="20"/>
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
