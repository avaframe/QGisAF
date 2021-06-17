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
    <rasterrenderer classificationMin="0" band="1" classificationMax="100" type="singlebandpseudocolor" opacity="1" nodataColor="" alphaBand="-1">
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
        <colorrampshader maximumValue="100" clip="0" classificationMode="2" colorRampType="DISCRETE" minimumValue="0" labelPrecision="6">
          <colorramp type="gradient" name="[source]">
            <Option type="Map">
              <Option type="QString" name="color1" value="255,0,255,0"/>
              <Option type="QString" name="color2" value="140,2,115,255"/>
              <Option type="QString" name="discrete" value="0"/>
              <Option type="QString" name="rampType" value="gradient"/>
              <Option type="QString" name="stops" value="0.01;255,0,255,0:0.166667;95,226,188,255:0.333333;128,197,95,255:0.5;156,150,28,255:0.666667;153,99,48,255:0.833333;148,56,77,255"/>
            </Option>
            <prop v="255,0,255,0" k="color1"/>
            <prop v="140,2,115,255" k="color2"/>
            <prop v="0" k="discrete"/>
            <prop v="gradient" k="rampType"/>
            <prop v="0.01;255,0,255,0:0.166667;95,226,188,255:0.333333;128,197,95,255:0.5;156,150,28,255:0.666667;153,99,48,255:0.833333;148,56,77,255" k="stops"/>
          </colorramp>
          <item label="&lt;= 1,000000" color="#ff00ff" alpha="0" value="1"/>
          <item label="1,000000 - 16,666667" color="#5fe2bc" alpha="255" value="16.666666666666668"/>
          <item label="16,666667 - 33,333333" color="#80c55f" alpha="255" value="33.333333333333336"/>
          <item label="33,333333 - 50,000000" color="#9c961c" alpha="255" value="50"/>
          <item label="50,000000 - 66,666667" color="#996330" alpha="255" value="66.66666666666667"/>
          <item label="66,666667 - 83,333333" color="#94384d" alpha="255" value="83.33333333333334"/>
          <item label="> 83,333333" color="#8c0273" alpha="255" value="inf"/>
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
