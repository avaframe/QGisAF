<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.18.3-Zürich" hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" maxScale="1000" minScale="1e+08">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal enabled="0" fetchMode="0" mode="0">
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
      <resampling zoomedOutResamplingMethod="nearestNeighbour" zoomedInResamplingMethod="nearestNeighbour" enabled="false" maxOversampling="2"/>
    </provider>
    <rasterrenderer classificationMin="1" band="1" classificationMax="1000" type="singlebandpseudocolor" opacity="0.698" nodataColor="" alphaBand="-1">
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
        <colorrampshader maximumValue="1000" clip="0" classificationMode="1" colorRampType="DISCRETE" minimumValue="1" labelPrecision="0">
          <colorramp type="gradient" name="[source]">
            <Option type="Map">
              <Option type="QString" name="color1" value="250,204,250,0"/>
              <Option type="QString" name="color2" value="1,25,89,255"/>
              <Option type="QString" name="discrete" value="0"/>
              <Option type="QString" name="rampType" value="gradient"/>
              <Option type="QString" name="stops" value="0.00900901;250,204,250,255:0.024024;242,157,107,255:0.049049;130,130,49,255:0.0990991;33,96,97,255"/>
            </Option>
            <prop v="250,204,250,0" k="color1"/>
            <prop v="1,25,89,255" k="color2"/>
            <prop v="0" k="discrete"/>
            <prop v="gradient" k="rampType"/>
            <prop v="0.00900901;250,204,250,255:0.024024;242,157,107,255:0.049049;130,130,49,255:0.0990991;33,96,97,255" k="stops"/>
          </colorramp>
          <item label="&lt;= 1" color="#faccfa" alpha="0" value="1"/>
          <item label="1 - 10" color="#faccfa" alpha="255" value="10"/>
          <item label="10 - 25" color="#f29d6b" alpha="255" value="25"/>
          <item label="25 - 50" color="#828231" alpha="255" value="50"/>
          <item label="50 - 100" color="#216061" alpha="255" value="100"/>
          <item label="> 100" color="#011959" alpha="255" value="inf"/>
          <rampLegendSettings direction="0" suffix="" useContinuousLegend="1" orientation="2" prefix="" minimumLabel="" maximumLabel="">
            <numericFormat id="basic">
              <Option type="Map">
                <Option type="QChar" name="decimal_separator" value=""/>
                <Option type="int" name="decimals" value="6"/>
                <Option type="int" name="rounding_type" value="0"/>
                <Option type="bool" name="show_plus" value="false"/>
                <Option type="bool" name="show_thousand_separator" value="true"/>
                <Option type="bool" name="show_trailing_zeros" value="false"/>
                <Option type="QChar" name="thousand_separator" value=""/>
              </Option>
            </numericFormat>
          </rampLegendSettings>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast gamma="1" brightness="0" contrast="0"/>
    <huesaturation grayscaleMode="0" saturation="0" colorizeRed="255" colorizeBlue="128" colorizeGreen="128" colorizeStrength="100" colorizeOn="0"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
